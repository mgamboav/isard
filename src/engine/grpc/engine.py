import grpc
from engine.grpc.proto import engine_pb2
from engine.grpc.proto import engine_pb2_grpc

from engine.grpc.lib.grpc_actions import GrpcActions

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
        engine_info = self.grpc.engine_info()	
        return engine_pb2.EngineStatusResponse(is_alive = engine_info['is_alive'],
												background_is_alive = engine_info['background_is_alive'],
												broom_thread_is_alive = engine_info['broom_thread_is_alive'],
												changes_domains_thread_is_alive = engine_info['changes_domains_thread_is_alive'],
												changes_hyps_thread_is_alive = engine_info['changes_hyps_thread_is_alive'],
												download_changes_thread_is_alive = engine_info['download_changes_thread_is_alive'],
												event_thread_is_alive = engine_info['event_thread_is_alive'],
												disk_operations_threads = engine_info['disk_operations_threads'],
												long_operations_threads = engine_info['long_operations_threads'],
												working_threads = engine_info['working_threads'],
												status_threads = engine_info['status_threads'])
        
