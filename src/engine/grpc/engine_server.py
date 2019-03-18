import grpc
import time
import hashlib
import engine_pb2
import engine_pb2_grpc
from concurrent import futures

# ~ from .controllers.grpc_actions import GrpcActions
 
class EngineServicer(engine_pb2_grpc.EngineServicer):
    """
    gRPC server for Engine Service
    """
    def __init__(self, *args, **kwargs):
        self.server_port = 46001
        # ~ self.grpc=GrpcActions()
 
    def DomainStart(self, request, context):
        print( 'received request to start domain')
        # ~ print(request)
        print(request.id)
        
        # ~ self.grpc.start_domain_from_id(request.domainID)
        
        result = {'result': True, 'status': 'Started'}
 
        return engine_pb2.actionResult(**result)
 
    def DomainStop(self, request, context):
        print( 'received request to stop domain')
        print(request.domainID)
        
        # ~ self.grpc.stop_domain_from_id(request.domainID)
        
        result = {'result': True, 'status': 'Stopped'}
 
        return engine_pb2.actionResult(**result)

    def DomainDelete(self, request, context):
        print( 'received request to delete domain')
        print(request.domainID)
        
        # ~ self.grpc.xxxxx(request.domainID)
        
        result = {'result': True, 'status': 'Stopped'}
 
        return engine_pb2.actionResult(**result) 

    def DomainCreateFromTemplate(self, request, context):
        print( 'received request to create domain')
        print(request)
        if 'domain_id' not in request.keys(): print ('No trobo el domain_id!!')
        if 'template_id' not in request.keys(): print ('No trobo la template_id!!')
        # ~ print(request.domainCreateFromTemplate)
        
        # ~ self.grpc.xxxxx(request.domainCreateFromTemplate)
        
        result = {'result': True, 'status': 'Stopped'}
 
        return engine_pb2.actionResult(**result) 
 
    def TemplateCreateFromDomain(self, request, context):
        print( 'received request to create template')
        print(request)
        print(request.templateCreateFromDomain)
        
        # ~ self.grpc.xxxxx(templateCreateFromDomain)
        
        result = {'result': True, 'status': 'Stopped'}
 
        return engine_pb2.actionResult(**result)
        
    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        engine_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 
        # This line can be ignored
        engine_pb2_grpc.add_EngineServicer_to_server(EngineServicer(),engine_server)
 
        # bind the server to the port defined above
        engine_server.add_insecure_port('[::]:{}'.format(self.server_port))
 
        # start the server
        engine_server.start()
        print ('Engine Server running ...')
 
        try:
            # need an infinite loop since the above
            # code is non blocking, and if I don't do this
            # the program will exit
            while True:
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            engine_server.stop(0)
            print('Engine Server Stopped ...')
 
curr_server = EngineServicer()
curr_server.start_server()
