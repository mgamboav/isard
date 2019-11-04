from api.grpc.grpc_server import GrpcServer
from test.engine_mock import EngineMock as Engine
from db.schema import create_schema
import time


import alembic.config
alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.main(argv=alembicArgs)

exit(1)

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
