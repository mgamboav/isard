import grpc
import time
import hashlib

from engine.grpc.proto import changes_pb2
from engine.grpc.proto import changes_pb2_grpc
    
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
    
MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class ChangesServicer(changes_pb2_grpc.ChangesServicer):
    """
    gRPC server for Changes stream Service
    """
    def __init__(self, app):
        self.server_port = 46001
        

    def DomainChanges(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                for c in r.table('domains').pluck('id','status').changes().run(conn):
                    # ~ if c['new_val']['status'] == 'Started':
                        # ~ yield {'domain_id':c['new_val']['id']}
                        yield changes_pb2.DomainChangesResponse(domain_id=c['new_val']['id'])
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return changes_pb2.DomainChangesResponse()  
