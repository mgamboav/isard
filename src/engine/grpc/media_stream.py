import grpc
from engine.grpc.proto import media_stream_pb2
from engine.grpc.proto import media_stream_pb2_grpc

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

from engine.grpc.media_sm import MediaSM, StateInvalidError
 
class MediaStreamServicer(media_stream_pb2_grpc.MediaStreamServicer):
    """
    gRPC server for Templates Changes stream Service
    """
    def __init__(self, app):
        self.media_sm = MediaSM()
        
    def Changes(self, request_iterator, context):
        try:
            with rdb() as conn:
                for c in r.table('media').pluck('id','status','detail').changes().run(conn):
                    ''' DELETED '''
                    if c['new_val'] is None:
                        yield media_stream_pb2.MediaStreamResponse( media_id=c['old_val']['id'],
                                                                        state='DELETED',
                                                                        detail=c['old_val']['detail'],
                                                                        next_actions=[])
                        continue
                    ''' NEW '''
                    if c['old_val'] is None:
                        yield media_stream_pb2.MediaStreamResponse( media_id=c['new_val']['id'],
                                                                        state='NEW',
                                                                        detail=c['new_val']['detail'],
                                                                        next_actions=[])
                        continue
                    
                    ''' Is it a valid state? '''
                    if c['new_val']['status'].upper() not in self.media_sm.get_states(): continue
                    
                    ''' Is it a detail update? '''
                    if c['old_val']['status'] == c['new_val']['status']: continue
                    
                    new_state=c['new_val']['status'].upper()
                    yield media_stream_pb2.MediaStreamResponse( media_id=c['new_val']['id'],
                                                                    state=new_state,
                                                                    detail=c['new_val']['detail'],
                                                                    next_actions=self.media_sm.get_next_actions(new_state))  
        except StateInvalidError:
            context.set_details('State invalid: ')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return media_stream_pb2.MediaStreamResponse()  
        except Exception as e:
            print(e)
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return media_stream_pb2.MediaStreamResponse()  
