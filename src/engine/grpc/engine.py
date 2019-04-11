import grpc
from engine.grpc.proto import engine_pb2
from engine.grpc.proto import engine_pb2_grpc

from google.protobuf.json_format import MessageToDict

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

from engine.grpc.lib.grpc_actions import GrpcActions

class EngineServicer(engine_pb2_grpc.EngineServicer):
    """
    gRPC server for Engine Service
    """
    def __init__(self, app):
        self.manager = app.m
        self.grpc = GrpcActions(self.manager)
        
    def IsAlive(self, request, context):
        return engine_pb2.IsAliveResponse(is_alive = self.grpc.engine_info()['is_alive'])
        
    def Status(self, request, context):
        engine_info = self.grpc.engine_info()	
        return engine_pb2.StatusResponse(is_alive = engine_info['is_alive'],
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
        
    def Config(self, request, context):
        config_new = MessageToDict(request, preserving_proto_field_name=True)
        with rdb() as conn:
            config_db = r.table('config').get(1).pluck('engine').run(conn)['engine']
            # ~ del config_db['engine']['grafana']
            # ~ import pprint
            # ~ pprint.pprint(config_db)
            # ~ return engine_pb2.ConfigResponse()
            return engine_pb2.ConfigResponse(intervals = config_db['intervals'],
                                            ssh = config_new['ssh'], #config_db['ssh'],
                                            stats = config_db['stats'],
                                            log = config_db['log'],
                                            timeouts = config_db['timeouts'])
