import grpc
import time
import hashlib

from engine.grpc.proto import desktop_pb2_grpc
from engine.grpc.proto import desktops_stream_pb2_grpc
from engine.grpc.proto import templates_pb2_grpc
from engine.grpc.proto import templates_stream_pb2_grpc
from engine.grpc.proto import media_pb2_grpc
from engine.grpc.proto import media_stream_pb2_grpc
from engine.grpc.proto import engine_pb2_grpc

from concurrent import futures

from engine.grpc.desktop import DesktopServicer
from engine.grpc.desktops_stream import DesktopsStreamServicer
from engine.grpc.templates import TemplatesServicer
from engine.grpc.templates_stream import TemplatesStreamServicer
from engine.grpc.media import MediaServicer
from engine.grpc.media_stream import MediaStreamServicer
from engine.grpc.engine import EngineServicer


class GrpcServer(object):
    def __init__(self, app):
        self.app = app
        self.server_port = 1313
        self.engine_grpc_server = None
        
    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        self.engine_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        desktop_pb2_grpc.add_DesktopServicer_to_server(DesktopServicer(self.app),self.engine_grpc_server)
        desktops_stream_pb2_grpc.add_DesktopsStreamServicer_to_server(DesktopsStreamServicer(self.app),self.engine_grpc_server)        
        templates_pb2_grpc.add_TemplatesServicer_to_server(TemplatesServicer(self.app),self.engine_grpc_server)
        templates_stream_pb2_grpc.add_TemplatesStreamServicer_to_server(TemplatesStreamServicer(self.app),self.engine_grpc_server)  
        media_pb2_grpc.add_MediaServicer_to_server(MediaServicer(self.app),self.engine_grpc_server)
        media_stream_pb2_grpc.add_MediaStreamServicer_to_server(MediaStreamServicer(self.app),self.engine_grpc_server) 
        engine_pb2_grpc.add_EngineServicer_to_server(EngineServicer(self.app),self.engine_grpc_server)

        # bind the server to the port defined above
        self.engine_grpc_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        self.engine_grpc_server.start()
        return True
        
    def stop_server(self):
        self.engine_grpc_server.stop(0)
