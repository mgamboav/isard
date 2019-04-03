import grpc
import time
import hashlib

from engine.grpc.proto import domains_stream_pb2
from engine.grpc.proto import domains_stream_pb2_grpc
    
from concurrent import futures

import rethinkdb as r
from rethinkdb.errors import (
    ReqlAuthError,
    ReqlCursorEmpty,
    ReqlDriverError,
    ReqlError,
    ReqlInternalError,
    ReqlNonExistenceError,
    ReqlOpFailedError,
    ReqlOpIndeterminateError,
    ReqlPermissionError,
    ReqlQueryLogicError,
    ReqlResourceLimitError,
    ReqlRuntimeError,
    ReqlServerCompileError,
    ReqlTimeoutError,
    ReqlUserError)

from engine.grpc.database import rdb
# ~ from engine.grpc.grpc_actions import GrpcActions

from engine.grpc.domain_actions import DomainActions, StateInvalidError
from engine.grpc.helpers import get_viewer
    
MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class DomainsStreamServicer(domains_stream_pb2_grpc.DomainsStreamServicer):
    """
    gRPC server for Changes stream Service
    """
    def __init__(self, app):
        self.server_port = 46001
        self.domain_actions = DomainActions()
        
    def Changes(self, request_iterator, context):
        ''' Checks '''
        print(self.domain_actions.get_states())
        import pprint
        try:
            with rdb() as conn:
                for c in r.table('domains').pluck('id','kind','status','detail','viewer').changes().run(conn):
                    ''' DELETED '''
                    if c['new_val'] is None:
                        yield domains_stream_pb2.DomainsStreamResponse( domain_id=c['old_val']['id'],
                                                                        state='DELETED',
                                                                        detail=c['old_val']['detail'],
                                                                        kind=c['old_val']['kind'],
                                                                        next_actions=[])
                        continue
                    ''' NEW '''
                    if c['old_val'] is None:
                        yield domains_stream_pb2.DomainsStreamResponse( domain_id=c['new_val']['id'],
                                                                        state='NEW',
                                                                        detail=c['new_val']['detail'],
                                                                        kind=c['new_val']['kind'],
                                                                        next_actions=[])
                        continue
                    
                    ''' Is it a valid state? '''
                    if c['new_val']['status'].upper() not in self.domain_actions.get_states(): continue
                    
                    ''' Is it a detail or viewer update? '''
                    if c['old_val']['status'] == c['new_val']['status']:
                        continue
                    
                    new_state=c['new_val']['status'].upper()
                    print('NEW_STATE: '+new_state)
                    
                    ''' Is it a desktop? '''
                    if c['new_val']['kind'] == 'desktop':
                        ''' If it is an started state return also the viewer '''
                        if new_state == 'STARTED':
                            yield domains_stream_pb2.DomainsStreamResponse( domain_id=c['new_val']['id'],
                                                                            state=new_state,
                                                                            detail=c['new_val']['detail'],
                                                                            kind=c['new_val']['kind'],
                                                                            next_actions=self.domain_actions.get_next_actions(new_state),
                                                                            viewer=get_viewer(c['new_val']['viewer']))
                        else:
                            yield domains_stream_pb2.DomainsStreamResponse( domain_id=c['new_val']['id'],
                                                                            state=new_state,
                                                                            detail=c['new_val']['detail'],
                                                                            kind=c['new_val']['kind'],
                                                                            next_actions=self.domain_actions.get_next_actions(new_state))  
                    ''' It is a template or base '''
                    else:
                        
                        
                    
        except StateInvalidError:
            context.set_details('State invalid: ')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return domains_stream_pb2.DomainsStreamResponse()  
        except Exception as e:
            print(e)
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return domains_stream_pb2.DomainsStreamResponse()  
