import unittest
import grpc
from concurrent import futures

from engine.grpc.proto import desktop_pb2, desktop_pb2_grpc

class RPCDestopServerTest(unittest.TestCase):
    from engine.grpc.desktop import DesktopServicer
    server_class = DesktopServicer
    port = 50051
    actions = ['STOP','START','PAUSE','RESUME','DELETE','UPDATE','TEMPLATE']

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        desktop_pb2_grpc.add_DesktopServicer_to_server(self.server_class(None), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()

    def tearDown(self):
        self.server.stop(None)




    def test_list(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.List(desktop_pb2.ListRequest())
        # ~ print(response.desktops)
        self.assertEqual(response.desktops, ['_admin_downloaded_slax93', '_admin_downloaded_tetros', '_admin_asdfasdfas', '_admin_downloaded_zxspectrum'])

    def test_get(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = desktop_pb2_grpc.DesktopStub(channel)
            response = stub.Get(desktop_pb2.GetRequest(desktop_id='_admin_downloaded_slax93'))
        # ~ print(response.desktops)
        self.assertEqual(response.next_actions, [2, 5, 6, 7])
        # ~ self.assertEqual(response.desktop, ['_admin_downloaded_slax93', '_admin_downloaded_tetros', '_admin_asdfasdfas', '_admin_downloaded_zxspectrum'])

if __name__ == '__main__':
    unittest.main()
