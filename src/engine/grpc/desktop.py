import grpc
import time
import hashlib
import json

import sys,os
#from engine.services.log import logs

from engine.grpc.proto import desktop_pb2
from engine.grpc.proto import desktop_pb2_grpc
    
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

from engine.grpc.lib.database import rdb
from engine.grpc.lib.grpc_actions import GrpcActions


from engine.grpc.statemachines.desktop_sm import DesktopSM, StateInvalidError
from engine.grpc.lib.helpers import get_viewer

# ~ from engine.services.threads.eq_hyp_worker import eq_hyp_worker
    
MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class DesktopServicer(desktop_pb2_grpc.DesktopServicer):
    """
    gRPC server for Templates Service
    """
    def __init__(self, app):
        self.server_port = 46001
        # ~ self.grpc = GrpcActions(self.manager)
        self.engine_actions = GrpcActions(app.m)
        self.desktop_sm = DesktopSM()
        self.app = app
        

    def List(self, request, context):
        try:
            with rdb() as conn:
                desktops = list(r.table('domains').get_all('desktop', index='kind').pluck('id').run(conn))
                desktops = [d['id'] for d in desktops]
            return desktop_pb2.ListResponse(desktops=desktops)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'List error: \n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.ListResponse()  

    def Get(self, request, context):
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).run(conn)
            if len(desktop) == 0:
                context.set_details(request.desktop_id+'  not found in database.')
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return desktop_pb2.GetResponse()                     
            next_actions=self.desktop_sm.get_next_actions(desktop['status'].upper())
            return desktop_pb2.GetResponse(desktop=json.dumps(desktop), next_actions=next_actions)   ##json.dumps(list(desktop)) This returns root keys only
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return desktop_pb2.GetResponse()             
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Get error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.GetResponse() 
                              
    def Start(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.desktop_id).pluck('status','kind').run(conn)
            next_actions = self.desktop_sm.get_next_actions(domain['status'].upper())
            if 'START' not in next_actions:    
            # ~ if domain['status'] not in ['Stopped','Failed']: 
                context.set_details(request.desktop_id+' is '+domain['status']+' and can\'t be started from this state.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.StartResponse()
            elif domain['kind'] != 'desktop':
                context.set_details(request.desktop_id+' is a '+domain['kind']+'.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                   
                return desktop_pb2.StartResponse()
        except StateInvalidError:
            context.set_details('State '+domain['status'].upper()+' unknown')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return desktop_pb2.StartResponse()           
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return desktop_pb2.StartResponse()            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Start error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.StartResponse()
            
        ''' Start desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.start_domain_from_id(request.desktop_id)
            print('STARTING FROM ENGINE')
            result = self.engine_actions.start_domain_from_id(request.desktop_id)
            self.app.loop.call_soon_threadsafe(self.app.qq.put_nowait, {'process':'parallel','action':'start_domain_inside_desktop.py','domain':'_admin_tetros'})
            if result is not False:
                return desktop_pb2.StartResponse(state='STARTED', \
                                        viewer=result,
                                        next_actions=self.desktop_sm.get_next_actions('STARTED'))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Start error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return desktop_pb2.StartResponse()
            
                                                
            # ~ ''' DATABASE '''
            # ~ with rdb() as conn:
                # ~ r.table('domains').get(request.desktop_id).update({'status':'Starting'}).run(conn)
                # ~ # with rdb() as conn:
                # ~ c = r.table('domains').get_all(r.args(['Started','Failed']),index='status').filter({'id':request.desktop_id}).pluck('status','viewer').changes().run(conn)
                # ~ state=c.next(MIN_TIMEOUT)
            # ~ next_actions = self.desktop_sm.get_next_actions(state['new_val']['status'].upper())
            # ~ viewer=get_viewer(state['new_val']['viewer'])
            # ~ return desktop_pb2.StartResponse(state=state['new_val']['status'].upper(),viewer=viewer,next_actions=next_actions)
            # ~ # return desktop_pb2.StartResponse(state='STARTED',viewer=viewer,next_actions=next_actions)
            # ~ # return desktop_pb2.StartResponse()
        # ~ except ReqlTimeoutError:
            # ~ context.set_details('Not able to start the domain '+request.desktop_id)
            # ~ context.set_code(grpc.StatusCode.DEADLINE_EXCEEDED)             
            # ~ return desktop_pb2.StartResponse()  
        # ~ # except ReqlNonExistenceError:
            # ~ # context.set_details(request.desktop_id+' domain not found')
            # ~ # context.set_code(grpc.StatusCode.INTERNAL)             
            # ~ # return desktop_pb2.StartResponse()             
        # ~ except Exception as e:
            # ~ exc_type, exc_obj, exc_tb = sys.exc_info()
            # ~ fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Start error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            # ~ context.set_details(str(e))
            # ~ context.set_code(grpc.StatusCode.UNKNOWN)             
            # ~ return desktop_pb2.StartResponse()

    def Viewer(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.desktop_id).pluck('status','kind','viewer').run(conn)
            next_actions = self.desktop_sm.get_next_actions(domain['status'].upper())
            if 'STOP' not in next_actions:                  
            # ~ if domain['status'] not in ['Started']: 
                context.set_details(request.desktop_id+' is '+domain['status']+' and can\'t have viewer in this state.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.StartResponse()
            elif domain['kind'] != 'desktop':
                context.set_details(request.desktop_id+' is a '+domain['kind']+'.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                   
                return desktop_pb2.StartResponse()
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return desktop_pb2.StartResponse()            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Viewer error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.StartResponse()
            
        ''' get viewer for desktop_id '''
        viewer=get_viewer(domain['viewer'])
        return desktop_pb2.ViewerResponse(state=domain['status'].upper(),viewer=viewer)
             
    def Stop(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                domain = r.table('domains').get(request.desktop_id).pluck('status','kind').run(conn)
            next_actions = self.desktop_sm.get_next_actions(domain['status'].upper())
            if 'STOP' not in next_actions:                  
            # ~ if domain['status'] not in ['Started']: 
                context.set_details(request.desktop_id+' is '+domain['status']+' and can\'t be stopped from this state.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.StopResponse()
            elif domain['kind'] != 'desktop':
                context.set_details(request.desktop_id+' is a '+domain['kind']+'.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.StopResponse()                
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return desktop_pb2.StopResponse()         
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Stop error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database!')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.StopResponse()
            
        ''' Stop desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.stop_domain_from_id(request.desktop_id)
            print('STOPPING FROM ENGINE')
            print(self.engine_actions.stop_domain_from_id(request.desktop_id))
        
                    
            print('XXXXXXXXXXXXXXXXXXXX')
            return desktop_pb2.StopResponse(state='STOPPED',next_actions=[2,3])
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.desktop_id).update({'status':'Stopping'}).run(conn)
                with rdb() as conn:
                    c = r.table('domains').get_all(r.args(['Stopped','Failed']),index='status').filter({'id':request.desktop_id}).pluck('status').changes().run(conn)
                    state=c.next(MIN_TIMEOUT)
                next_actions = self.desktop_sm.get_next_actions(state['new_val']['status'].upper())
                return desktop_pb2.StopResponse(state=state['new_val']['status'].upper(),next_actions=next_actions)



                # ~ with rdb() as conn:
                    # ~ c = r.table('domains').get_all(r.args(['Stopped']),index='status').filter({'id':request.desktop_id}).pluck('status').changes().run(conn)
                    # ~ state=c.next(MIN_TIMEOUT)
                    # ~ next_actions = self.domain_actions.for_desktop(request.desktop_id,state['new_val']['status'])
                # ~ return desktop_pb2.StopResponse(state=state['new_val']['status'].upper(), next_actions=next_actions)
                return desktop_pb2.StopResponse()
        # ~ except ReqlTimeoutError:
            # ~ context.set_details('Not able to stop the domain')
            # ~ context.set_code(grpc.StatusCode.INTERNAL)             
            # ~ return desktop_pb2.StopResponse() 
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' domain not found.')
            context.set_code(grpc.StatusCode.INTERNAL)             
            return desktop_pb2.StopResponse()                        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Stop error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return desktop_pb2.StopResponse()

    def Delete(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).pluck('status','kind').run(conn)
            if desktop['status'] in ['Started','Starting']: 
                context.set_details('It is started.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.DeleteResponse()
            elif desktop['kind'] != 'desktop':
                context.set_details('It is not a desktop.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.DeleteResponse()                
        except ReqlNonExistenceError:
            context.set_details(desktop_id+'  not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return desktop_pb2.DeleteResponse()         
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'Delete error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.DeleteResponse()
        
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
                return desktop_pb2.DeleteResponse(state='DELETED')
        except ReqlTimeoutError:
            context.set_details('Unable to delete the domain '+request.desktop_id)
            context.set_code(grpc.StatusCode.INTERNAL)             
            return desktop_pb2.DeleteResponse()            
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return desktop_pb2.DeleteResponse()


    def FromTemplate(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).pluck('id').run(conn)
            context.set_details(request.desktop_id+' already exists in system.')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
            return desktop_pb2.FromTemplateResponse()                
        except ReqlNonExistenceError:
            pass        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'FromTemplate error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.FromTemplateResponse()
        try:
            with rdb() as conn:
                template = r.table('domains').get(request.template_id).without('history_domain').run(conn)
            if template['status'] not in ['Stopped']: 
                context.set_details(request.template_id+' it is not stopped.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.FromTemplateResponse()
            elif template['kind'] == 'desktop':
                context.set_details(request.template_id+' it is not a template.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return desktop_pb2.FromTemplateResponse()                
        except ReqlNonExistenceError:
            context.set_details(request.template_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return desktop_pb2.FromTemplateResponse()         
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'FromTemplate error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.FromTemplateResponse()
        
        ''' OPTIONAL HARDWARE VALUES | GET FROM TEMPLATE '''
        hardware = {}
        hardware['vcpus'] = int(template['create_dict']['hardware']['vcpus']) if request.hardware.vcpus == 0 else request.hardware.vcpus
        hardware['memory'] = int(template['create_dict']['hardware']['memory']) if request.hardware.memory == 0 else request.hardware.memory
        hardware['videos'] = template['create_dict']['hardware']['videos'] if len(request.hardware.videos) == 0 else request.hardware.videos
        hardware['graphics'] = template['create_dict']['hardware']['graphics'] if len(request.hardware.graphics) == 0 else request.hardware.graphics
        hardware['boot_order'] = template['create_dict']['hardware']['boot_order'] if len(request.hardware.boots) == 0 else request.hardware.boots
        hardware['interfaces'] = template['create_dict']['hardware']['interfaces'] if len(request.hardware.interfaces) == 0 else request.hardware.interfaces
        hardware['isos'] = template['create_dict']['hardware']['isos'] if len(request.hardware.isos) == 0 else request.hardware.isos
        hardware['floppies'] = template['create_dict']['hardware']['floppies'] if len(request.hardware.floppies) == 0 else request.hardware.floppies
        ## Check for .qcow in boot_disk_rpath??   
        hardware['disks']=[{'file': request.desktop_id + '.qcow2' if request.hardware.boot_disk_rpath == '' else request.hardware.boot_disk_rpath,
                            'parent':template['hardware']['disks'][0]['file']}]    
        # ~ if request.hardware.boot_disk_bus == '': request.hardware.boot_disk_bus = 'virtio'

        desktop = { 'id': request.desktop_id,
                    'kind': 'desktop',
                    'status': 'Creating',
                    'create_dict': {'hardware':hardware, 
                                    'origin': request.template_id}, 
                    'hypervisors_pools': template['hypervisors_pools']}

        ''' Add desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.add_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').insert(desktop).run(conn)
                c=r.table('domains').get(request.desktop_id).changes().filter({'new_val':{'status':'Stopped'}}).run(conn) 
                c.next(MAX_TIMEOUT)
                next_actions = action[state['new_val']['status'].capitalize()]
                return desktop_pb2.FromTemplateResponse(state='STOPPED', next_actions=next_actions)
        except ReqlTimeoutError:
            context.set_details('Unable to create the domain '+request.desktop_id)
            context.set_code(grpc.StatusCode.INTERNAL)             
            return desktop_pb2.FromTemplateResponse()            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'FromTemplate error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return desktop_pb2.FromTemplateResponse()
