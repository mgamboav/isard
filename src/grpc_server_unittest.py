import unittest
import grpc
import time
import hashlib

from engine.grpc.proto import desktop_pb2


from engine.grpc.proto import desktop_pb2_grpc
from engine.grpc.proto import desktops_stream_pb2_grpc
from engine.grpc.proto import template_pb2_grpc
from engine.grpc.proto import templates_stream_pb2_grpc
from engine.grpc.proto import media_pb2_grpc
from engine.grpc.proto import media_stream_pb2_grpc
from engine.grpc.proto import engine_pb2_grpc

from concurrent import futures

from engine.grpc.desktop import DesktopServicer
from engine.grpc.desktops_stream import DesktopsStreamServicer
from engine.grpc.template import TemplateServicer
from engine.grpc.templates_stream import TemplatesStreamServicer
from engine.grpc.media import MediaServicer
from engine.grpc.media_stream import MediaStreamServicer
from engine.grpc.engine import EngineServicer


class GrpcServerTest(unittest.TestCase):
    host = 'localhost'
    server_port = 54100

    # instantiate a communication channel
    # ~ self.channel = grpc.insecure_channel(
                    # ~ '{}:{}'.format(self.host, self.server_port))
        
    def setUp(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        self.app=None
        self.engine_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        desktop_pb2_grpc.add_DesktopServicer_to_server(DesktopServicer(self.app),self.engine_grpc_server)
        desktops_stream_pb2_grpc.add_DesktopsStreamServicer_to_server(DesktopsStreamServicer(self.app),self.engine_grpc_server)        
        template_pb2_grpc.add_TemplateServicer_to_server(TemplateServicer(self.app),self.engine_grpc_server)
        templates_stream_pb2_grpc.add_TemplatesStreamServicer_to_server(TemplatesStreamServicer(self.app),self.engine_grpc_server)  
        media_pb2_grpc.add_MediaServicer_to_server(MediaServicer(self.app),self.engine_grpc_server)
        media_stream_pb2_grpc.add_MediaStreamServicer_to_server(MediaStreamServicer(self.app),self.engine_grpc_server) 
        # ~ engine_pb2_grpc.add_EngineServicer_to_server(EngineServicer(self.app),self.engine_grpc_server)

        # bind the server to the port defined above
        self.engine_grpc_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        self.engine_grpc_server.start()
        return True
        
    def tearDown(self):
        self.engine_grpc_server.stop(0)

    def test_desktop_list(self):
        with grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port)) as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.List(desktop_pb2.ListRequest())
        self.assertEqual(len(response.desktops), 2)

if __name__ == '__main__':
    unittest.main()
