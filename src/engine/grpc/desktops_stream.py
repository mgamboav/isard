import grpc
from engine.grpc.proto import desktops_stream_pb2
from engine.grpc.proto import desktops_stream_pb2_grpc

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
from engine.grpc.lib.database import rdb

from engine.grpc.statemachines.desktops_sm import DesktopsSM, StateInvalidError
from engine.grpc.lib.helpers import get_viewer


class DesktopsStreamServicer(desktops_stream_pb2_grpc.DesktopsStreamServicer):
    """
    gRPC server for Domain Changes stream Service
    """
    def __init__(self, app):
        self.desktops_sm = DesktopsSM()
        
    def Changes(self, request_iterator, context):
        try:
            with rdb() as conn:
                for c in r.table('domains').get_all('desktop', index='kind').pluck('id','status','detail','viewer').changes().run(conn):
                    ''' DELETED '''
                    if c['new_val'] is None:
                        yield desktops_stream_pb2.DesktopsStreamResponse( desktop_id=c['old_val']['id'],
                                                                        state='DELETED',
                                                                        detail=c['old_val']['detail'] if 'detail' in c['old_val'].keys() else '',
                                                                        next_actions=[])
                        continue
                    ''' NEW '''
                    if c['old_val'] is None:
                        yield desktops_stream_pb2.DesktopsStreamResponse( desktop_id=c['new_val']['id'],
                                                                        state='NEW',
                                                                        detail=c['new_val']['detail'] if 'detail' in c['new_val'].keys() else '',
                                                                        next_actions=[])
                        continue
                    
                    ''' Is it a valid state? '''
                    if c['new_val']['status'].upper() not in self.desktops_sm.get_states(): continue

                    new_state=c['new_val']['status'].upper()                    
                    
                    ''' I the viewer event comes from libvirt after the domain is updated to started
                        we could have a problem '''
                    if new_state == 'STARTED':
                        if 'viewer' not in c['new_val'].keys(): continue
                        ''' Sometimes could happen with some domains at first event'''
                        if c['new_val']['viewer']['hostname'] is False: continue
                        yield desktops_stream_pb2.DesktopsStreamResponse( desktop_id=c['new_val']['id'],
                                                                        state=new_state,
                                                                        detail=c['new_val']['detail'],
                                                                        next_actions=self.desktops_sm.get_next_actions(new_state),
                                                                        viewer=get_viewer(c['new_val']['viewer']))                        
                    else:
                        ''' Is it a detail or viewer update? '''
                        if c['old_val']['status'] == c['new_val']['status']:
                            continue
                        ''' It could happen that at maximum start/stop speed the domain
                            sends an Starting event but there are updates yet to come to
                            the Stopped domain (remove the viewer??) '''
                        if c['old_val']['status'] == 'Starting' and c['new_val']['status'] == 'Stopped':
                            continue
                        yield desktops_stream_pb2.DesktopsStreamResponse( desktop_id=c['new_val']['id'],
                                                                        state=new_state,
                                                                        detail=c['new_val']['detail'],
                                                                        next_actions=self.desktops_sm.get_next_actions(new_state))  
        except StateInvalidError:
            context.set_details('State invalid: ')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktops_stream_pb2.DesktopsStreamResponse()  
        except Exception as e:
            print(e)
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktops_stream_pb2.DesktopsStreamResponse()  
