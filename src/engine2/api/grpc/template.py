import grpc
import time

from api.grpc.proto import template_pb2
from api.grpc.proto import template_pb2_grpc
import engine.engine_exceptions

MIN_TIMEOUT = 5  # Start/Stop/delete
MAX_TIMEOUT = 10 # Creations...
 
class TemplateServicer(template_pb2_grpc.TemplateServicer):
    """
    gRPC service for Templates
    """
    def __init__(self, engine):
        self.server_port = 46001
        self.engine = engine

    def Get(self, request, context):
        ''' Gets template_id with all data '''
        try:
            fields = [] if request.fields is None else request.fields
            state, template, next_actions = self.engine.TemplateGet(request.template_id, fields)
            return template_pb2.GetResponse(state=state, Template=Template, next_actions=next_actions)
        except NonExistenceError:
            context.set_details(request.template_id+' not found in database.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return template_pb2.GetResponse()             
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Get error: {request.template_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.GetResponse() 

    def GetState(self, request, context):
        ''' Gets template_id only with state '''
        try:
            state, next_actions = self.engine.TemplateGetState(request.template_id)
            return template_pb2.GetStateResponse(state=state, next_actions=next_actions)
        except NonExistenceError:
            context.set_details(request.template_id+' not found in database.')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return template_pb2.GetStateResponse()             
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Get error: {request.template_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')
            
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.GetStateResponse() 
                    
    def List(self, request, context):
        ''' Gets list of Template dicts with all keys/values '''
        try:
            template_ids = [] if request.template_ids is None else request.template_ids
            fields = [] if request.fields is None else request.fields
            prefix = '' if request.prefix is None else request.prefix
            Templates = self.engine.TemplateList(template_ids, fields, prefix)
            return template_pb2.ListResponse(Templates=Templates)  
        except:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.ListResponse()             

    def ListState(self, request, context):
        ''' Gets list of Template dicts with all keys/values '''
        try:
            template_ids = [] if request.template_ids is None else request.template_ids
            prefix = '' if request.prefix is None else request.prefix
            Templates = self.engine.TemplateListState(template_ids, prefix)
            return template_pb2.ListStateResponse(Templates=Templates)  
        except:
            context.set_details('Unable to access database.')
            context.set_code(grpc.StatusCode.INTERNAL)               
            return template_pb2.ListResponse() 

    def Delete(self, request, context):
        try:
            state = self.engine.TemplateDelete(request.template_id)
            return template_pb2.DeleteResponse(state=state)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'Delete error: {request.template_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return template_pb2.DeleteResponse()

    def FromDesktop(self, request, context):
        try:             
            state, next_actions = self.engine.TemplateFromDesktop(request.template_id, request.desktop_id, request.hardware)
            return template_pb2.FromDesktopResponse(state=state, next_actions=next_actions)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ logs.grpc.error(f'FromTemplate error: {request.template_id}\n Type: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)             
            return template_pb2.FromDesktopResponse()

    
