import grpc
import time
import hashlib

from engine.grpc.proto import desktops_pb2_grpc
from engine.grpc.proto import templates_pb2_grpc
from engine.grpc.proto import engine_pb2_grpc
from engine.grpc.proto import domains_stream_pb2_grpc

from concurrent import futures

from engine.grpc.desktops import DesktopsServicer
from engine.grpc.templates import TemplatesServicer
from engine.grpc.domains_stream import DomainsStreamServicer
from engine.grpc.engine import EngineServicer


class GrpcServer(object):
    def __init__(self, app):
        self.app = app
        self.server_port = 46001
        self.engine_grpc_server = None
        
    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        self.engine_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        desktops_pb2_grpc.add_DesktopsServicer_to_server(DesktopsServicer(self.app),self.engine_grpc_server)
        templates_pb2_grpc.add_TemplatesServicer_to_server(TemplatesServicer(self.app),self.engine_grpc_server)
        engine_pb2_grpc.add_EngineServicer_to_server(EngineServicer(self.app),self.engine_grpc_server)
        domains_stream_pb2_grpc.add_DomainsStreamServicer_to_server(DomainsStreamServicer(self.app),self.engine_grpc_server)

        # bind the server to the port defined above
        self.engine_grpc_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        self.engine_grpc_server.start()
        return True
        
    def stop_server(self):
        self.engine_grpc_server.stop(0)
