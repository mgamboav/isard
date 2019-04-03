import grpc
import time
import hashlib

from engine.grpc.proto import desktops_pb2_grpc
from engine.grpc.proto import templates_pb2_grpc
from engine.grpc.proto import engineinfo_pb2_grpc
from engine.grpc.proto import changes_pb2_grpc

from concurrent import futures

from engine.grpc.desktops import DesktopsServicer
from engine.grpc.templates import TemplatesServicer
from engine.grpc.engineinfo import EngineInfoServicer
from engine.grpc.changes import ChangesServicer

class GrpcServer(object):
    def __init__(self, app):
        self.app = app
        self.server_port = 46001
        
    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        engine_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # This line can be ignored
        desktops_pb2_grpc.add_DesktopsServicer_to_server(DesktopsServicer(self.app),engine_grpc_server)
        templates_pb2_grpc.add_TemplatesServicer_to_server(TemplatesServicer(self.app),engine_grpc_server)
        engineinfo_pb2_grpc.add_EngineInfoServicer_to_server(EngineInfoServicer(self.app),engine_grpc_server)
        changes_pb2_grpc.add_ChangesServicer_to_server(ChangesServicer(self.app),engine_grpc_server)

        # bind the server to the port defined above
        engine_grpc_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        engine_grpc_server.start()
        print ('Engine GRPC Server running ...')
        try:
            # need an infinite loop since the above
            # code is non blocking, and if I don't do this
            # the program will exit
            while True:
                # ~ time.sleep(2)
                # ~ print(self.grpc.engine_info())
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            engine_grpc_server.stop(0)
            print('Engine GRPC Server Stopped ...')
