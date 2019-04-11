import unittest
import grpc
from google.protobuf.json_format import MessageToDict
import time
import hashlib

from engine.grpc.proto import desktop_pb2
from engine.grpc.proto import desktops_stream_pb2
from engine.grpc.proto import template_pb2
from engine.grpc.proto import templates_stream_pb2
from engine.grpc.proto import media_pb2
from engine.grpc.proto import media_stream_pb2
from engine.grpc.proto import engine_pb2


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

from engine.models.manager_hypervisors import ManagerHypervisors

class App(object):
    def __init():
        None
        

app = App()
app.m = ManagerHypervisors()

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
        self.app=app
        self.engine_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        desktop_pb2_grpc.add_DesktopServicer_to_server(DesktopServicer(self.app),self.engine_grpc_server)
        desktops_stream_pb2_grpc.add_DesktopsStreamServicer_to_server(DesktopsStreamServicer(self.app),self.engine_grpc_server)        
        template_pb2_grpc.add_TemplateServicer_to_server(TemplateServicer(self.app),self.engine_grpc_server)
        templates_stream_pb2_grpc.add_TemplatesStreamServicer_to_server(TemplatesStreamServicer(self.app),self.engine_grpc_server)  
        media_pb2_grpc.add_MediaServicer_to_server(MediaServicer(self.app),self.engine_grpc_server)
        media_stream_pb2_grpc.add_MediaStreamServicer_to_server(MediaStreamServicer(self.app),self.engine_grpc_server) 
        engine_pb2_grpc.add_EngineServicer_to_server(EngineServicer(self.app),self.engine_grpc_server)

        # bind the server to the port defined above
        self.engine_grpc_server.add_insecure_port('[::]:{}'.format(self.server_port))

        # start the server
        self.engine_grpc_server.start()
        # ~ time.sleep(5)
        return True
        
    def tearDown(self):
        self.engine_grpc_server.stop(0)


    ''' ENGINE TESTS '''
    
    def test_engine_IsAlive(self):
        with grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port)) as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            response = stub.IsAlive(engine_pb2.IsAliveRequest())
        self.assertEqual(response.is_alive, True)

    def test_engine_Status(self):
        with grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port)) as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            response = MessageToDict(stub.Status(engine_pb2.StatusRequest()), preserving_proto_field_name=True)
        response_ok = {'is_alive':True,
                        'background_is_alive': True,
                        'broom_thread_is_alive': True,
                        'changes_domains_thread_is_alive': True,
                        'changes_hyps_thread_is_alive': True,
                        'download_changes_thread_is_alive': True,
                        'event_thread_is_alive': True,
                        'disk_operations_threads': ['isard-hypervisor'],
                        'long_operations_threads': ['isard-hypervisor']}
                        # ~ 'working_threads': [],
                        # ~ 'status_threads': []}
        self.assertEqual(response, response_ok)

    def test_engine_Config(self):
        with grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port)) as channel:
            stub = engine_pb2_grpc.EngineStub(channel)

            cfg = {'intervals': {'background_polling': 10,
                                   'status_polling': 10,
                                   'test_hyp_fail': 20,
                                   'time_between_polling': 5,
                                   'transitional_states_polling': 2},
                     'log': {'log_file': 'msg.log', 'log_level': 'WARNING', 'log_name': 'isard'},
                     'ssh': {'paramiko_host_key_policy_check': False},
                     'stats': {'active': True,
                               'hyp_stats_interval': 5,
                               'max_queue_domains_status': 10,
                               'max_queue_hyps_status': 10},
                     'timeouts': {'libvirt_hypervisor_timeout_connection': 3,
                                  'retries_hyp_is_alive': 3,
                                  'ssh_paramiko_hyp_test_connection': 4,
                                  'timeout_between_retries_hyp_is_alive': 1,
                                  'timeout_hypervisor': 10,
                                  'timeout_queues': 2,
                                  'timeout_trying_hyp_and_ssh': 10,
                                  'timeout_trying_ssh': 2}}            
            response = MessageToDict(stub.Config(engine_pb2.ConfigRequest(intervals = cfg['intervals'],
                                                                        ssh = cfg['ssh'],
                                                                        log = cfg['log'],
                                                                        stats = cfg['stats'],
                                                                        timeouts = cfg['timeouts'])), 
                                                                        preserving_proto_field_name=True)
            response['ssh'] = cfg['ssh'] #############################################################              
        self.assertDictEqual(response, cfg)
        
        
    ''' DESKTOP TESTS '''
    
    
    def test_desktop_list(self):
        with grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port)) as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.List(desktop_pb2.ListRequest())
        self.assertEqual(len(response.desktops), 6)


        
if __name__ == '__main__':
    print('Waiting 2 seconds to let engine be stable...')
    time.sleep(2)
    unittest.main()
