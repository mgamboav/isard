from api.grpc.grpc_server import GrpcServer
from test.grpc.engine_mock import EngineMock as Engine
import time

def reset_schema():
    import psycopg2
    import sys

    """
    Drop all tables of database you given.
    """
    reset_db='''DROP SCHEMA IF EXISTS public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO isardvdi;
    GRANT ALL ON SCHEMA public TO public;
    COMMENT ON SCHEMA public IS 'standard public schema';'''

    try:
        conn = psycopg2.connect("host='isard-database' dbname='engine' user='isardvdi' password='isardvdi'")
        conn.set_isolation_level(0)
    except Exception as e:
        print(str(e))
        print("Unable to connect to the database.")

    cur = conn.cursor()

    try:
        cur.execute(reset_db)
        cur.close()
        conn.close()
    except:
        print("Error: ", sys.exc_info()[1])
    
reset_schema()

import alembic.config
alembicArgs = [
    '--raiseerr',
    'downgrade', '-1',
]
try:
    alembic.config.main(argv=alembicArgs)
except Exception as e:
    print(e)
    pass
    
    
alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.main(argv=alembicArgs)

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
