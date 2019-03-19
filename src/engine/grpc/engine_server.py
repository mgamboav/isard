import grpc
import time
import hashlib
import engine_pb2
import engine_pb2_grpc
from concurrent import futures

import rethinkdb as r
from rethinkdb.errors import (
    ReqlAuthError,
    ReqlCursorEmpty,
    ReqlDriverError,
    ReqlError,
    ReqlInternalError,
    ReqlNonExistenceError,
    ReqlOpFailedError,
    ReqlOpIndeterminateError,
    ReqlPermissionError,
    ReqlQueryLogicError,
    ReqlResourceLimitError,
    ReqlRuntimeError,
    ReqlServerCompileError,
    ReqlTimeoutError,
    ReqlUserError)
    
# ~ from ..services.db import new_rethink_connection, close_rethink_connection
    
# ~ from .controllers.grpc_actions import GrpcActions

class rdb():
    def __init__(self, RETHINK_HOST='localhost', RETHINK_PORT=28015, RETHINK_DB='isard'):
        self.conn = None
        self.rh=RETHINK_HOST
        self.rp=RETHINK_PORT
        self.rb=RETHINK_DB
    def __enter__(self):
        self.conn = r.connect(self.rh, self.rp, db=self.rb)
        return self.conn
    def __exit__(self, type, value, traceback):
        self.conn.close()
        
 
class EngineServicer(engine_pb2_grpc.EngineServicer):
    """
    gRPC server for Engine Service
    """
    def __init__(self, *args, **kwargs):
        self.server_port = 46001
        # ~ self.grpc=GrpcActions()
 
    def DomainStart(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.domain_id).pluck('status','kind').run(conn)
            if len(domain)==0: 
                result = {'result': False, 'status': 'domain_id not found in database.'}
                return engine_pb2.actionResult(**result)
            elif domain['status'] not in ['Stopped','Failed']: 
                result = {'result': False, 'status': 'It is not in stopped or failed status'}
                return engine_pb2.actionResult(**result)
            elif domain['kind'] != 'desktop':
                result = {'result': False, 'status': 'You don\'t want to start a template.'}
                return engine_pb2.actionResult(**result)
        except Exception as e:
            result = {'result': False, 'status': 'Unable to access database.'}
            return engine_pb2.actionResult(**result)
        grpc.start_domain_from_id(request.domai
        ''' Start domain_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.start_domain_from_id(request.domain_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.domain_id).update({'status':'Starting'}).run(conn)
        except:
            result = {'result': False, 'status': 'Unable to start this domain now.'}
            return engine_pb2.actionResult(**result)
        result = {'result': True, 'status': 'Starting'}
        return engine_pb2.actionResult(**result)
 
    def DomainStop(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.domain_id).pluck('status','kind').run(conn)
            if domain['status'] not in ['Started']: 
                result = {'result': False, 'status': 'It is not started.'}
                return engine_pb2.actionResult(**result)
            elif domain['kind'] != 'desktop':
                result = {'result': False, 'status': 'You don\'t want to mess status in templates.'}
                return engine_pb2.actionResult(**result)
        except ReqlNonExistenceError:
            result = {'result': False, 'status': 'domain_id not found in database.'}
            return engine_pb2.actionResult(**result)         
        except Exception as e:
            print(e)
            result = {'result': False, 'status': 'Unable to access database.'}
            return engine_pb2.actionResult(**result)
        
        ''' Stop domain_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.stop_domain_from_id(request.domain_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.domain_id).update({'status':'Stopping'}).run(conn)
        except:
            result = {'result': False, 'status': 'Unable to stop this domain now.'}
            return engine_pb2.actionResult(**result)
        result = {'result': True, 'status': 'Stopping'}
        return engine_pb2.actionResult(**result)

    def DomainDelete(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.domain_id).pluck('status','kind').run(conn)
            if domain['status'] in ['Started','Starting']: 
                result = {'result': False, 'status': 'It is started.'}
                return engine_pb2.actionResult(**result)
            elif domain['kind'] != 'desktop':
                result = {'result': False, 'status': 'You don\'t want to delete a template.'}
                return engine_pb2.actionResult(**result)
        except ReqlNonExistenceError:
            result = {'result': False, 'status': 'domain_id not found in database.'}
            return engine_pb2.actionResult(**result)         
        except Exception as e:
            print(e)
            result = {'result': False, 'status': 'Unable to access database.'}
            return engine_pb2.actionResult(**result)
        
        ''' Delete domain_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.delete_domain_from_id(request.domain_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.domain_id).update({'status':'Deleting'}).run(conn)
        except:
            result = {'result': False, 'status': 'Unable to delete this domain now.'}
            return engine_pb2.actionResult(**result)
        result = {'result': True, 'status': 'Deleting'}
        return engine_pb2.actionResult(**result)

    def DomainCreateFromTemplate(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                template = r.table('domains').get(request.template_id).pluck('status','kind').run(conn)
            if template['kind'] == 'desktop':
                result = {'result': False, 'status': 'You don\'t want to create a desktop from a desktop.'}
                return engine_pb2.actionResult(**result)
        except ReqlNonExistenceError:
            result = {'result': False, 'status': 'domain_id not found in database.'}
            return engine_pb2.actionResult(**result)         
        except Exception as e:
            print(e)
            result = {'result': False, 'status': 'Unable to access database.'}
            return engine_pb2.actionResult(**result)

        ''' Check for all hardware in request or get the one in template '''
        # ~ try:
            # ~ hardware=request.hardware
        # ~ except:
            # ~ hardware=template['hardware']
        
            
        ''' Create domain_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.create_domain_from_template(request.domain_id)
            ''' DATABASE '''
            # ~ with rdb() as conn:
                # ~ r.table('domains').insert({'status':'Deleting'}).run(conn)
            None
        except:
            result = {'result': False, 'status': 'Unable to delete this domain now.'}
            return engine_pb2.actionResult(**result)
        result = {'result': True, 'status': 'Deleting'}
        return engine_pb2.actionResult(**result)
 
    def TemplateCreateFromDomain(self, request, context):
        print( 'received request to create template')
        print(request)
        print(request.domain_id)
        
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
        print ('Engine Server running ...')kers=10))
 
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
