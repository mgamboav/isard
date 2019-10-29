import grpc


import sys,os,json
from engine.services.log import logs

from engine.grpc.proto import template_pb2
from engine.grpc.proto import template_pb2_grpc

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

# ~ from engine.grpc.grpc_actions import GrpcActions

from engine.grpc.statemachines.desktop_sm import DesktopSM, StateInvalidError
# ~ from engine.grpc.statemachines.template_sm import TemplateSM, StateInvalidError

MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...

class TemplateServicer(template_pb2_grpc.TemplateServicer):
    """
    gRPC server for Templates Service
    """
    def __init__(self, app):
        # ~ self.grpc = GrpcActions(self.manager)
        self.desktop_sm = DesktopSM()
        # ~ self.template_sm = TemplateSM()
    

    def List(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                templates = list(r.table('domains').filter(r.row['kind'].match("template")).pluck('id').run(conn))
                templates = [t['id'] for t in templates]
            return template_pb2.ListResponse(templates=templates)
        except Exception as e:
            print(e)
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.ListResponse()  

    def Get(self, request, context):
        ''' Checks '''
        try:
            with rdb() as conn:
                template = r.table('domains').get(request.template_id).run(conn)
            if len(template) == 0:
                context.set_details(request.template_id+'  not found in database.')
                context.set_code(grpc.StatusCode.UNKNOWN)
                return template_pb2.GetResponse()                     
            # ~ desktop['next_actions']=self.domain_actions.for_desktop(request.template_id,desktop['status'])
            return template_pb2.GetResponse(template=template)
        except ReqlNonExistenceError:
            context.set_details(request.template_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return template_pb2.GetResponse()             
        except Exception as e:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.GetResponse() 
            
    def FromDesktop(self, request, context):
        return self.TemplateAndBaseFromDesktop('template', request, context)
        
    # ~ def BaseFromDesktop(self, request, context):
        # ~ return self.TemplateAndBaseFromDesktop('base', request, context)
                
    def TemplateAndBaseFromDesktop(self, kind, request, context):
        ''' Checks '''
        if request.template_id == '':
            context.set_details('Missing template_id in call to templating from desktop: '+request.desktop_id)
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
            return template_pb2.FromDesktopResponse() 
        try:
            with rdb() as conn:
                template = r.table('domains').get(request.template_id).pluck('id').run(conn)
            context.set_details(request.template_id+' already exists in system.')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
            return template_pb2.FromDesktopResponse()                
        except ReqlNonExistenceError:
            pass        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'FromDesktop error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.FromDesktopResponse()
        try:
            with rdb() as conn:
                desktop = r.table('domains').get(request.desktop_id).without('history_domain').run(conn)
            if desktop['status'] not in ['Stopped']: 
                context.set_details(request.desktop_id+' it is not stopped.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return template_pb2.FromDesktopResponse()
            elif desktop['kind'] != 'desktop':
                context.set_details(request.desktop_id+' it is not a desktop.')
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)                
                return template_pb2.FromDesktopResponse()                
        except ReqlNonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return template_pb2.FromDesktopResponse()         
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'FromDesktop error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.FromDesktopResponse()
        
        ''' OPTIONAL HARDWARE VALUES | GET FROM DESKTOP '''
        hardware = {}
        hardware['vcpus'] = int(desktop['create_dict']['hardware']['vcpus']) if request.hardware.vcpus == 0 else request.hardware.vcpus
        hardware['memory'] = int(desktop['create_dict']['hardware']['memory']) if request.hardware.memory == 0 else request.hardware.memory
        hardware['videos'] = desktop['create_dict']['hardware']['videos'] if len(request.hardware.videos) == 0 else request.hardware.videos
        hardware['graphics'] = desktop['create_dict']['hardware']['graphics'] if len(request.hardware.graphics) == 0 else request.hardware.graphics
        hardware['boot_order'] = desktop['create_dict']['hardware']['boot_order'] if len(request.hardware.boots) == 0 else request.hardware.boots
        hardware['interfaces'] = desktop['create_dict']['hardware']['interfaces'] if len(request.hardware.interfaces) == 0 else request.hardware.interfaces
        hardware['isos'] = desktop['create_dict']['hardware']['isos'] if len(request.hardware.isos) == 0 and 'isos' in desktop['create_dict']['hardware'].keys() else request.hardware.isos
        hardware['floppies'] = desktop['create_dict']['hardware']['floppies'] if len(request.hardware.floppies) == 0  and 'floppies' in desktop['create_dict']['hardware'].keys() else request.hardware.floppies
        ## Check for .qcow in boot_disk_rpath??   
        hardware['disks']=[{'file': request.template_id + '.qcow2' if request.hardware.boot_disk_rpath == '' else request.hardware.boot_disk_rpath,
                            'parent':''}]    
        # ~ if request.hardware.boot_disk_bus == '': request.hardware.boot_disk_bus = 'virtio'
                           
        ''' Create a new minimal domain inside template_dict '''
        create_dict=desktop['create_dict']
        create_dict['origin']=request.desktop_id
        create_dict['template_dict']={ 'id': request.template_id,
                                        'kind': kind,
                                        'hypervisors_pools': desktop['hypervisors_pools'],
                                        'create_dict': {'hardware': hardware}}
                                        
        ''' Add template_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.add_template_from_desktop(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(request.desktop_id).update({'create_dict':create_dict,'status':'CreatingTemplate'}).run(conn)
                # ~ r.table('domains').get(request.desktop_id).update({'create_dict':create_dict}).run(conn)
                c=r.table('domains').get(request.desktop_id).changes().filter({'new_val':{'status':'Stopped'}}).run(conn) 
                state=c.next(MAX_TIMEOUT)
                if r.table('domains').get(request.template_id).run(conn) is None:
                    context.set_details('Disk for template already exists')
                    context.set_code(grpc.StatusCode.FAILED_PRECONDITION)             
                    return template_pb2.FromDesktopResponse()            
            extra_fields = json.loads(request.extra_fields_json)
            if extra_fields is not '':
                r.table('domains').get(request.template_id).update(extra_fields).run(conn)
            next_actions = self.desktop_sm.get_next_actions(state['new_val']['status'].upper())
            return template_pb2.FromDesktopResponse(state='STOPPED', next_actions=next_actions)
        except ReqlTimeoutError:
            context.set_details('Unable to create the domain '+request.template_id)
            context.set_code(grpc.StatusCode.DEADLINE_EXCEEDED)             
            return template_pb2.FromDesktopResponse()            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logs.grpc.error(f'FromDesktop error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)             
            return template_pb2.FromDesktopResponse()


