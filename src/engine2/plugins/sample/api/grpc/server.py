import grpc
# ~ import time
# ~ import hashlib
from concurrent import futures

from api.grpc.proto import domain_pb2_grpc
# ~ from api.grpc.proto import desktops_stream_pb2_grpc
# ~ from api.grpc.proto import template_pb2_grpc
# ~ from api.grpc.proto import templates_stream_pb2_grpc
# ~ from api.grpc.proto import base_pb2_grpc
# ~ from api.grpc.proto import bases_stream_pb2_grpc
# ~ from api.grpc.proto import media_pb2_grpc
# ~ from api.grpc.proto import media_stream_pb2_grpc
# ~ from api.grpc.proto import engine_pb2_grpc

from api.grpc.domain import DomainServicer
# ~ from api.grpc.desktops_stream import DesktopsStreamServicer
# ~ from api.grpc.template import TemplateServicer
# ~ from api.grpc.templates_stream import TemplatesStreamServicer
# ~ from api.grpc.base import BaseServicer
# ~ from api.grpc.bases_stream import BasesStreamServicer
# ~ from api.grpc.media import MediaServicer
# ~ from api.grpc.media_stream import MediaStreamServicer
# ~ from api.grpc.engine import EngineServicer


class GrpcServer(object):
    def __init__(self, engine):
        self.engine = engine
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

        domain_pb2_grpc.add_DomainServicer_to_server(DomainServicer(self.engine),self.engine_grpc_server)
        # ~ desktops_stream_pb2_grpc.add_DesktopsStreamServicer_to_server(DesktopsStreamServicer(self.app),self.engine_grpc_server)        
        # ~ template_pb2_grpc.add_TemplateServicer_to_server(TemplateServicer(self.app),self.engine_grpc_server)
        # ~ templates_stream_pb2_grpc.add_TemplatesStreamServicer_to_server(TemplatesStreamServicer(self.app),self.engine_grpc_server)  
        # ~ base_pb2_grpc.add_BaseServicer_to_server(BaseServicer(self.app),self.engine_grpc_server)
        # ~ bases_stream_pb2_grpc.add_BasesStreamServicer_to_server(BasesStreamServicer(self.app),self.engine_grpc_server) 
        # ~ media_pb2_grpc.add_MediaServicer_to_server(MediaServicer(self.app),self.engine_grpc_server)
        # ~ media_stream_pb2_grpc.add_MediaStreamServicer_to_server(MediaStreamServicer(self.app),self.engine_grpc_server) 
        # ~ engine_pb2_grpc.add_EngineServicer_to_server(EngineServicer(self.app),self.engine_grpc_server)

        # bind the server to the port defined above
        self.engine_grpc_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        self.engine_grpc_server.start()
        return True
        
    def stop_server(self):
        self.engine_grpc_server.stop(0)
