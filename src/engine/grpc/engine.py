import grpc
from engine.grpc.proto import engine_pb2
from engine.grpc.proto import engine_pb2_grpc

from engine.grpc.grpc_actions import GrpcActions

MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class EngineServicer(engine_pb2_grpc.EngineServicer):
    """
    gRPC server for Engine Service
    """
    def __init__(self, app):
        self.manager = app.m
        self.grpc = GrpcActions(self.manager)
        
    def EngineIsAlive(self, request, context):
        return engine_pb2.EngineIsAliveResponse(is_alive = self.grpc.engine_info()['is_alive'])
        
    def EngineStatus(self, request, context):
        return engine_pb2.EngineStatuseResponse(self.grpc.engine_info())
        
