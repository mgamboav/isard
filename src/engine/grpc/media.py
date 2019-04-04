import grpc
from engine.grpc.proto import media_pb2
from engine.grpc.proto import media_pb2_grpc

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
# ~ from engine.grpc.grpc_actions import GrpcActions


from engine.grpc.statemachines.media_sm import MediaSM, StateInvalidError

    
MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class MediaServicer(media_pb2_grpc.MediaServicer):
    """
    gRPC server for Media Service
    """
    def __init__(self, app):
        # ~ self.grpc = GrpcActions(self.manager)
        self.media_sm = MediaSM()
        

    def MediaList(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                media = list(r.table('media').pluck('id').run(conn))
                media = [d['id'] for d in medias]
            return media_pb2.MediaListResponse(media=media)
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return media_pb2.MediaListResponse()  

    def MediaGet(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                Media = r.table('media').get(request.media_id).run(conn)
            if len(Media) == 0:
                context.set_details(request.media_id+'  not found in database.')
                context.set_code(grpc.StatusCode.UNKNOWN)
                return media_pb2.MediaStartResponse()                     
            Media['next_actions']=self.media_sm.get_next_actions(request.media_id,Media['status'].upper())
            return media_pb2.MediaGetResponse(Media=Media)
        except ReqlNonExistenceError:
            context.set_details(request.media_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return media_pb2.MediaStartResponse()             
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return media_pb2.MediaStartResponse() 
                                         
    def MediaDelete(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                Media = r.table('domains').get(request.media_id).pluck('status','kind').run(conn)
            if Media['status'] in ['Started','Starting']: 
                context.set_details('It is started.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return media_pb2.MediaDeleteResponse()
            elif Media['kind'] != 'Media':
                context.set_details('It is not a Media.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return media_pb2.MediaDeleteResponse()                
        except ReqlNonExistenceError:
            context.set_details(media_id+'  not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return media_pb2.MediaDeleteResponse()         
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return media_pb2.MediaDeleteResponse()
        
        ''' Delete media_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.delete_domain_from_id(request.media_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.media_id).update({'status':'Deleting'}).run(conn)
                with rdb() as conn:
                    c=r.table('domains').get(request.media_id).changes().filter({'new_val':None}).run(conn) 
                    c.next(MIN_TIMEOUT)
                return media_pb2.MediaDeleteResponse(state='DELETED')
        except ReqlTimeoutError:
            context.set_details('Unable to delete the domain '+request.media_id)
            context.set_code(grpc.StatusCode.INTERNAL)             
            return media_pb2.MediaDeleteResponse()            
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return media_pb2.MediaDeleteResponse()
