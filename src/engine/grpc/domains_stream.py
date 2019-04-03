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

from engine.grpc.domain_actions import DomainActions
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
                for c in r.table('domains').get_all(r.args(self.domain_actions.get_states()),index='status').pluck('id','kind','status','detail','viewer').changes().run(conn):
                    #~ pprint.pprint(c)
                    if c['new_val'] is None: continue
                    if c['old_val'] is not None and c['old_val']['status'] == c['new_val']['status']: continue
                    new_state=c['new_val']['status'].upper()
                    print('new state')
                    print(new_state)
                    print(new_state.upper())
                    print(self.domain_actions.get_next_actions(new_state))                    
                    if c['new_val']['kind'] == 'desktop':
                        #~ if self.domain_actions.valid_state(new_state):
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
        except Exception as e:
            print(e)
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return domains_stream_pb2.DomainsStreamResponse()  
