import grpc
import time, sys, os

from api.grpc.proto import domain_pb2
from api.grpc.proto import domain_pb2_grpc
from common.exceptions.engine import NotFoundError

import logging
log = logging.getLogger(__name__)

MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...

class DomainServicer(domain_pb2_grpc.DomainServicer):
    """
    gRPC service for Desktops
    """
    def __init__(self, engine):
        self.server_port = 46001
        self.engine = engine

    def VideoList(self, request, context):
        ''' Gets desktop videos in system with all data '''
        try:
            videos_pb = self.engine.desktop.video_list(pb=True)
            return desktop_pb2.VideoListResponse(videos=videos_pb)            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.error(f'VideoList error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details(f'VideoList error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.VideoListResponse() 

    def BootList(self, request, context):
        ''' Gets desktop videos in system with all data '''
        try:
            boots_pb = self.engine.desktop.boot_list(pb=True)
            return desktop_pb2.BootListResponse(boots=boots_pb)            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Get error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details(f'BootList error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.BootListResponse() 

    def InterfaceList(self, request, context):
        ''' Gets desktop videos in system with all data '''
        try:
            interfaces_pb = self.engine.desktop.interface_list(pb=True)
            return desktop_pb2.InterfaceListResponse(interfaces=interfaces_pb)            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Get error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details(f'BootList error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.InterfaceListResponse() 
            
    def Get(self, request, context):
        ''' Gets desktop_id with all data '''
        try:
            state, desktop, next_actions = self.engine.DesktopGet(request.desktop_id)
            return desktop_pb2.GetResponse(state=state, desktop=desktop, next_actions=next_actions)
        # ~ except NonExistenceError:
            # ~ context.set_details(request.desktop_id+' not found in database.')
            # ~ context.set_code(grpc.StatusCode.NOT_FOUND)
            # ~ return desktop_pb2.GetResponse()             
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Get error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details(f'Get error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.GetResponse() 

    def GetState(self, request, context):
        ''' Gets desktop_id only with state '''
        try:
            state, next_actions = self.engine.DesktopGetState(request.desktop_id)
            return desktop_pb2.GetStateResponse(state=state, next_actions=next_actions)
        except NonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return desktop_pb2.GetStateResponse()             
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Get error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.GetStateResponse() 
                    
    def List(self, request, context):
        ''' Gets list of desktop dicts with all keys/values '''
        try:
            domains = self.engine.domain.list(pb=True)
            # ~ print(self.engine.domain.list())
            return domain_pb2.ListResponse(domains=domains)  
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)               
            return domain_pb2.ListResponse()             

    def ListState(self, request, context):
        ''' Gets list of desktop dicts with all keys/values '''
        try:
            desktop_ids = [] if request.desktop_ids is None else request.desktop_ids
            prefix = '' if request.prefix is None else request.prefix
            desktops = self.engine.DesktopListState(desktop_ids, prefix)
            return desktop_pb2.ListStateResponse(desktops=desktops)  
        except:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.ListResponse() 
                                          
    def Start(self, request, context):
        try:
            state, viewer, next_actions = self.engine.DesktopStart(request.desktop_id)
            return desktop_pb2.StartResponse(state=state, \
                                        viewer=result,
                                        next_actions=next_actions)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Start error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return desktop_pb2.StartResponse()

    def Viewer(self, request, context):
        try:
            state, viewer, next_actions = self.engine.DesktopViewer(request.desktop_id)
            return desktop_pb2.ViewerResponse(state=state, viewer=viewer, next_actions=next_actions)
        except NonExistenceError:
            context.set_details(request.desktop_id+' not found in database.')
            context.set_code(grpc.StatusCode.UNKNOWN)
            return desktop_pb2.StartResponse()            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Viewer error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
                        
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return desktop_pb2.ViewerResponse()
 
    def Stop(self, request, context):
        try:
            state, next_actions = self.engine.DesktopStop(request.desktop_id)
            return desktop_pb2.StopResponse(state=state, \
                                        next_actions=next_actions)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Stop error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return desktop_pb2.StopResponse()

    def Delete(self, request, context):
        try:
            state = self.engine.DesktopDelete(request.desktop_id)
            return desktop_pb2.DeleteResponse(state=state)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Delete error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return desktop_pb2.DeleteResponse()

    def FromTemplate(self, request, context):
        try:             
            state, next_actions = self.engine.desktop.from_template(request.desktop_id, request.template_id, request.hardware)
            return desktop_pb2.FromTemplateResponse(state=state, next_actions=next_actions)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'FromTemplate error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return desktop_pb2.FromTemplateResponse()
                    
    def New(self, request, context):
        try:             
            state, next_actions = self.engine.desktop.new(request.desktop_id, request.template_id, request.hardware)
            return desktop_pb2.FromTemplateResponse(state=state, next_actions=next_actions)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'FromTemplate error: {request.desktop_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return desktop_pb2.FromTemplateResponse()
