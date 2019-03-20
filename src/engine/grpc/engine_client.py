import grpc
import engine_pb2
import engine_pb2_grpc

class EngineClient(object):
    """
    Client for accessing the gRPC functionality
    """
 
    def __init__(self):
        # configure the host and the
        # the port to which the client should connect
        # to.
        self.host = 'localhost'
        self.server_port = 46001
 
        # instantiate a communication channel
        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port))
 
        # bind the client to the server channel
        self.stub = engine_pb2_grpc.EngineStub(self.channel)
 
    def desktop_start(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopStart(engine_pb2.DesktopStartRequest(domain_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        print(response.state)
        return True

    def desktop_stop(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopStop(engine_pb2.DesktopStopRequest(domain_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStopResponse.State.STARTED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)
        print(response.state)
        return True

    def domain_delete(self, message):
        """
        Client function to call the rpc
        """
        to_engine_message = engine_pb2.Domain(domain_id=message)
        print(to_engine_message)
        result = self.stub.DomainDelete(to_engine_message)
        print(result)
        return result
                        
    def domain_create_from_id(self,message):
        print(message)
        to_engine_message = engine_pb2.domainCreateFromTemplate(domain_id=message['domain_id'],template_id='la template id')
        result = self.stub.DomainCreateFromTemplate(to_engine_message)
        return result
        
        
        

curr_client = EngineClient()

import time

while True:
    curr_client.desktop_start('_admin_downloaded_zxspectrum')
    #~ time.sleep(1)
    curr_client.desktop_stop('_admin_downloaded_zxspectrum')
# ~ curr_client.domain_delete('_admin_downloaded_tetros')


# ~ message = {'domain_id':'el id de nou domain','template_id':'el id de plantilla a derivar'}
# ~ curr_client.domain_create_from_id(message)
