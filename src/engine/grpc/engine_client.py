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
 
    def domain_start(self, message):
        """
        Client function to call the rpc
        """
        to_engine_message = engine_pb2.domainID(id=message)
        print(to_engine_message)
        result = self.stub.DomainStart(to_engine_message)
        print(result)
        return result

curr_client = EngineClient()

curr_client.domain_start('el_id_de_guais')
