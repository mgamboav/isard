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

MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
    
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

    def DesktopList(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                desktops = list(r.table('domains').get_all('desktop', index='kind').pluck('id').run(conn))
                desktops = [d['id'] for d in desktops]
            return engine_pb2.DesktopListResponse(desktops=desktops)
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopListResponse()  

    def DesktopGet(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).run(conn)
                print(desktop)
            if len(desktop) == 0:
                context.set_details(desktop_id+'  not found in database.')
                context.set_code(grpc.StatusCode.UNKNOWN)
                return engine_pb2.DesktopStartResponse()                     
            return engine_pb2.DesktopGetResponse(desktop=desktop)
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopStartResponse() 
                              
    def DesktopStart(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.desktop_id).pluck('status','kind').run(conn)
            if domain['status'] not in ['Stopped','Failed']: 
                context.set_details('It is not in stopped or failed status')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopStartResponse()
            elif domain['kind'] != 'desktop':
                context.set_details('You don\'t want to start a template.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                   
                return engine_pb2.DesktopStartResponse()
        except ReqlNonExistenceError:
            context.set_details(desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return engine_pb2.DesktopStartResponse()            
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopStartResponse()
            
        ''' Start desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.start_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.desktop_id).update({'status':'Starting'}).run(conn)
                with rdb() as conn:
                    c = r.table('domains').get_all(r.args(['Started','Failed']),index='status').filter({'id':request.desktop_id}).pluck('status').changes().run(conn)
                    state=c.next(MIN_TIMEOUT)
                return engine_pb2.DesktopStartResponse(state=state['new_val']['status'].upper())
        except ReqlTimeoutError:
            context.set_details('Not able to start the domain')
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopStartResponse()            
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopStartResponse()
 
    def DesktopStop(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.desktop_id).pluck('status','kind').run(conn)
            if domain['status'] not in ['Started']: 
                context.set_details(request.desktop_id+' it is not started.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopStopResponse()
            elif domain['kind'] != 'desktop':
                context.set_details(request.desktop_id+' it is not a desktop.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopStopResponse()                
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return engine_pb2.DesktopStopResponse()         
        except Exception as e:
            context.set_details('Unable to access database!')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopStopResponse()
            
        ''' Stop desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.stop_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.desktop_id).update({'status':'Stopping'}).run(conn)
                with rdb() as conn:
                    c = r.table('domains').get_all(r.args(['Stopped']),index='status').filter({'id':request.desktop_id}).pluck('status').changes().run(conn)
                    state=c.next(MIN_TIMEOUT)
                return engine_pb2.DesktopStopResponse(state=state['new_val']['status'].upper())
        except ReqlTimeoutError:
            context.set_details('Not able to stop the domain')
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopStopResponse()            
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopStopResponse()

    def DesktopDelete(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).pluck('status','kind').run(conn)
            if desktop['status'] in ['Started','Starting']: 
                context.set_details('It is started.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopDeleteResponse()
            elif desktop['kind'] != 'desktop':
                context.set_details('It is not a desktop.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopDeleteResponse()                
        except ReqlNonExistenceError:
            context.set_details(desktop_id+'  not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return engine_pb2.DesktopDeleteResponse()         
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopDeleteResponse()
        
        ''' Delete desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.delete_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.desktop_id).update({'status':'Deleting'}).run(conn)
                with rdb() as conn:
                    c=r.table('domains').get(request.desktop_id).changes().filter({'new_val':None}).run(conn) 
                    c.next(MIN_TIMEOUT)
                return engine_pb2.DesktopDeleteResponse(state='DELETED')
        except ReqlTimeoutError:
            context.set_details('Unable to delete the domain '+request.desktop_id)
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopDeleteResponse()            
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopDeleteResponse()


    def DesktopFromTemplate(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).pluck('id').run(conn)
            context.set_details(request.desktop_id+' already exists in system.')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
            return engine_pb2.DesktopFromTemplateResponse()                
        except ReqlNonExistenceError:
            pass        
        except Exception as e:
            print('1 '+str(e))
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopFromTemplateResponse()
        try:
            with rdb() as conn:
                template = r.table('domains').get(request.template_id).without('history_domain').run(conn)
            if template['status'] not in ['Stopped']: 
                context.set_details(request.template_id+' it is not stopped.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopFromTemplateResponse()
            elif template['kind'] == 'desktop':
                context.set_details(request.template_id+' it is not a template.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return engine_pb2.DesktopFromTemplateResponse()                
        except ReqlNonExistenceError:
            context.set_details(request.template_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return engine_pb2.DesktopFromTemplateResponse()         
        except Exception as e:
            print('2: '+str(e))
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.DesktopFromTemplateResponse()
        
        ''' OPTIONAL VALUES '''
        if not request.HasField("hardware"):
            print('before hardware')
            print(template['create_dict'])
            hardware = {"vcpus": template['create_dict']['hardware']['vcpus'],
                        "memory": template['create_dict']['hardware']['memory'],
                        "boot_order": template['create_dict']['hardware']['boot_order'],
                        "graphics": template['create_dict']['hardware']['graphics'],
                        "interfaces": template['create_dict']['hardware']['interfaces'],
                        "videos": template['create_dict']['hardware']['videos'],
                        "disks": [{ 'file':request.desktop_id+'.qcow2',
                                    'parent':template['hardware']['disks'][0]['file']}]}
        # ~ else:
            # ~ if not request.hardware.HasField("vcpus"): request.vcpus = template.create_dict.hardware.vcpus
            # ~ if not request.HasField("memory"): request.memory = template.create_dict.hardware.memory
            # ~ if not request.HasField("boot_disk_rpath"): request.boot_disk_rpath = request.desktop_id + '.qcow2'
            # ~ if not request.HasField("boot_diskbus"): request.boot_diskbus = template.create_dict.hardware.boot_diskbus
            # ~ if     len(request.videos) == 0: request.videos = template.create_dict.hardware.videos
            # ~ if     len(request.graphics) == 0: request.graphics = template.create_dict.hardware.graphics
            # ~ if     len(request.boots) == 0: request.boots = template.create_dict.hardware.boots
            # ~ if     len(request.interfaces) == 0: request.interfaces = template.create_dict.hardware.interfaces
            # ~ if     len(request.isos) == 0: request.isos = template.create_dict.hardware.isos
            # ~ if     len(request.floppies) == 0: request.floppies = template.create_dict.hardware.floppies
        desktop = { 'id': request.desktop_id,
                    'name': request.desktop_id,
                    'description': request.desktop_id,
                    'kind': 'desktop',
                    'user': 'admin',
                    'status': 'Creating',
                    'detail': None,
                    'category': 'local',
                    'group': 'local',
                    'xml': None,
                    'icon': 'debian',
                    'server': False,
                    'os': 'linux',
                    'options': {'viewers':{'spice':{'fullscreen':True}}},
                    'create_dict': {'hardware':hardware, 
                                    'origin': request.template_id}, 
                    'hypervisors_pools': template['hypervisors_pools'],
                    'allowed': {'roles': False,
                              'categories': False,
                              'groups': False,
                              'users': False}}

        ''' Add desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.add_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').insert(desktop).run(conn)
                with rdb() as conn:
                    c=r.table('domains').get(request.desktop_id).changes().filter({'new_val':{'status':'Stopped'}}).run(conn) 
                    c.next(MAX_TIMEOUT)
                return engine_pb2.DesktopFromTemplateResponse(state='STOPPED')
        except ReqlTimeoutError:
            context.set_details('Unable to create the domain '+request.desktop_id)
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopFromTemplateResponse()            
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return engine_pb2.DesktopFromTemplateResponse()


    def TemplateList(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                templates = list(r.table('domains').filter(r.row['kind'].match("template")).pluck('id').run(conn))
                templates = [t['id'] for t in templates]
            return engine_pb2.TemplateListResponse(templates=templates)
        except Exception as e:
            print(e)
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return engine_pb2.TemplateListResponse()  
 
 
 
 

        
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
