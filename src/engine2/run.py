from api.grpc.grpc_server import GrpcServer
from test.engine_mock import EngineMock as Engine

import time
# ~ from engine import Engine

engine = Engine()

''' GRPC api '''
grpc = GrpcServer(engine)
grpc.start_server()
print('GRPC server started...')
    
''' Loop as nothing is blocking '''
try:
    while True:
        time.sleep(60*60*60)
except KeyboardInterrupt:
    grpc.stop_server()
