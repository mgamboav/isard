import grpc
import time
import hashlib

from engine.grpc.proto import engine_pb2
from engine.grpc.proto import engine_pb2_grpc
    
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
from engine.grpc.grpc_actions import GrpcActions


from engine.grpc.domain_actions import DomainActions

    
MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class EngineServicer(engine_pb2_grpc.EngineServicer):
    """
    gRPC server for Engine Service
    """
    def __init__(self, app):
        self.server_port = 46001
        self.manager = app.m
        self.grpc = GrpcActions(self.manager)
        self.domain_actions = DomainActions()
        
    def EngineIsAlive(self, request, context):
        return engine_pb2.EngineIsAliveResponse(is_alive = self.grpc.engine_info()['is_alive'])
        
    def EngineStatus(self, request, context):
        return engine_pb2.EngineStatuseResponse(self.grpc.engine_info())
        
