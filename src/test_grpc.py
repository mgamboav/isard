import unittest
import grpc
import time
from concurrent import futures

from engine.grpc.proto import desktop_pb2, desktop_pb2_grpc
from engine.grpc.proto import template_pb2, template_pb2_grpc

from engine.grpc.proto import engine_pb2, engine_pb2_grpc

from engine.models.manager_hypervisors import ManagerHypervisors

class App(object):
    def __init():
        None
        
class RPCIsardServerTest(unittest.TestCase):
    from engine.grpc.desktop import DesktopServicer
    from engine.grpc.template import TemplateServicer
    from engine.grpc.engine import EngineServicer
    desktop_server_class = DesktopServicer
    template_server_class = TemplateServicer
    engine_server_class = EngineServicer
    
    port = 50051
    actions = ['STOP','START','PAUSE','RESUME','DELETE','UPDATE','TEMPLATE']

    # ~ enum State {
        # ~ UNKNOWN = 0;
        # ~ STOPPED = 1;
        # ~ STARTED = 2;
        # ~ PAUSED = 3;
        # ~ DELETED = 4;
        # ~ FAILED = 5;
    # ~ }
    
    app = App()
    ''' Manager Hypervisors '''
    app.m = ManagerHypervisors()
    time.sleep(5)
    
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        desktop_pb2_grpc.add_DesktopServicer_to_server(self.desktop_server_class(None), self.server)
        template_pb2_grpc.add_TemplateServicer_to_server(self.template_server_class(None), self.server)
        engine_pb2_grpc.add_EngineServicer_to_server(self.engine_server_class(self.app), self.server)
        
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        self.engine_test()

    def tearDown(self):
        self.server.stop(None)

    def engine_test(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            response = stub.EngineStatus(engine_pb2.EngineStatusRequest())  
        self.assertEqual(response.is_alive, True)
        # ~ self.assertEqual(response.background_is_alive, True)
        # ~ self.assertEqual(response.changes_domains_thread_is_alive, True)
        # ~ self.assertEqual(response.changes_hyps_thread_is_alive, True)
        # ~ self.assertEqual(response.changes_hyps_thread_is_alive, True)
        # ~ self.assertEqual(response.event_thread_is_alive, True) 
        
    def test_01get(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.Get(desktop_pb2.GetRequest(desktop_id='_admin_downloaded_tetros'))
        self.assertEqual(response.next_actions, [2, 5, 6, 7])

    def test_02list(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.List(desktop_pb2.ListRequest())
            domain = ['_admin_downloaded_tetros'] if '_admin_downloaded_tetros' in response.desktops else []
        self.assertListEqual(domain, ['_admin_downloaded_tetros'])

    def test_03start(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.Start(desktop_pb2.StartRequest(desktop_id='_admin_downloaded_tetros'))
        self.assertEqual(response.state, 2)
        # ~ self.assertEqual(response.next_actions, [2, 5, 6, 7])

    def test_04stop(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.Stop(desktop_pb2.StopRequest(desktop_id='_admin_downloaded_tetros'))
        self.assertEqual(response.state, 1)
        # ~ self.assertEqual(response.next_actions, [2, 5, 6, 7])

    def test_05templatingdefaults(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = template_pb2_grpc.TemplateStub(channel)
            response = stub.FromDesktop(template_pb2.FromDesktopRequest(desktop_id='_admin_downloaded_zxspectrum', template_id='_admin_grpc_test'))
        self.assertEqual(response.state, 1)
        # ~ self.assertEqual(response.next_actions, [2, 5, 6, 7])

    def test_06gettemplate(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = template_pb2_grpc.TemplateStub(channel)
            response = stub.Get(template_pb2.GetRequest(template_id='_admin_grpc_test'))
            self.assertEqual(response.state, 1)
        # ~ self.assertEqual(response.next_actions, [2, 5, 6, 7])
                        
if __name__ == '__main__':
    unittest.main()
