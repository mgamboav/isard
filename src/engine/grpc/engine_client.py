import grpc
import engine_pb2
import engine_pb2_grpc

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
from database import rdb

class EngineClient(object):
    """
    Client for accessing the gRPC functionality
    """
 
    def __init__(self):
        # configure the host and the
        # the port to which the client should connect
        # to.
        self.host = 'localhost'
        self.server_port = 46001
 
        # instantiate a communication channel
        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port))
 
        # bind the client to the server channel
        self.stub = engine_pb2_grpc.EngineStub(self.channel)

    def desktop_get(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopGet(engine_pb2.DesktopGetRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.desktop

    def desktop_list(self):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopList(engine_pb2.Empty())
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.desktops
                 
    def desktop_start(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopStart(engine_pb2.DesktopStartRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        print(response.state)
        print(response.viewer)
        return True

    def desktop_viewer(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopViewer(engine_pb2.DesktopViewerRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStopResponse.State.STARTED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)
        print(response.viewer)
        return True
        
    def desktop_stop(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopStop(engine_pb2.DesktopStopRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStopResponse.State.STARTED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)
        print(response.state)
        return True

    def desktop_delete(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.DesktopDelete(engine_pb2.DesktopDeleteRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStopResponse.State.STARTED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)
        print(response.state)
        return True

    def template_list(self):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.TemplateList(engine_pb2.Empty())
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.templates
                        
    def desktop_from_template(self,message):
        """
        PARAMETERS: name, description, user, category, group, icon, server,
        os, options '''
        
        """
        try:
            if 'hardware' in message.keys():
                response = self.stub.DesktopFromTemplate(engine_pb2.DesktopFromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id'], hardware=message['hardware']))
            else:
                response = self.stub.DesktopFromTemplate(engine_pb2.DesktopFromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id']))
        except grpc.RpcError as e:
            ## Should be deleted as it failed?##
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopFromTemplateResponse.State.STOPPED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)

        try:
            with rdb() as conn:
                template = r.table('domains').get(message['template_id']).pluck('id','name','description','user','category','group','icon','server','os','options').run(conn)             
        except ReqlNonExistenceError:
            return False       
        except Exception as e:
            print('2: '+str(e))
            context.set_details('Unable to access database.')
            return False           
        desktop = { 'name': message['desktop_id'].replace('_',' '),  ## PASS PARAMETER!
                    'description': 'the description',
                    'user': 'admin',
                    'category': 'admin',
                    'group': 'admin',
                    'icon': 'linux',
                    'server': False,
                    'os': 'linux',
                    'options': {'viewers':{'preferred':'spice','spice':{'fullscreen':True}}},
                    'allowed': {'private':True,
                                'roles': [],
                                'categories': [],
                                'groups': [],
                                'users': []}}    
                              
        ''' Add desktop_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.add_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(message['desktop_id']).update(desktop).run(conn)
                return True
        except ReqlTimeoutError:
            print(e)
            return False          
        except Exception as e:
            print(e)
            return False                                       
        print(response.state)
        return True

    def template_from_desktop(self,message):
        """
        PARAMETERS: name, description, user, category, group, icon, server,
        os, options '''
        
        """
        try:
            if 'hardware' in message.keys():
                response = self.stub.TemplateFromDesktop(engine_pb2.DesktopFromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id'], hardware=message['hardware']))
            else:
                response = self.stub.TemplateFromDesktop(engine_pb2.DesktopFromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id']))
        except grpc.RpcError as e:
            ## Should be deleted as it failed?##
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopFromTemplateResponse.State.STOPPED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)

        try:
            with rdb() as conn:
                desktop = r.table('domains').get(message['desktop_id']).pluck('id','name','description','user','category','group','icon','server','os','options').run(conn)             
        except ReqlNonExistenceError:
            return False       
        except Exception as e:
            print('2: '+str(e))
            context.set_details('Unable to access database.')
            return False           
        template = { 'name': message['template_id'].replace('_',' '),  ## PASS PARAMETER!
                    'description': 'the description',
                    'user': 'admin',
                    'category': 'admin',
                    'group': 'admin',
                    'icon': 'linux',
                    'server': False,
                    'os': 'linux',
                    'options': {'viewers':{'preferred':'spice','spice':{'fullscreen':True}}},
                    'allowed': {'private':True,
                                'roles': [],
                                'categories': [],
                                'groups': [],
                                'users': []}}    
                              
        ''' Add template_id '''
        try:
            ''' DIRECT TO ENGINE '''
            # ~ self.grpc.add_domain_from_id(request.desktop_id)
            ''' DATABASE '''
            with rdb() as conn:
                r.table('domains').get(message['template_id']).update(template).run(conn)
                import pprint
                pprint.pprint(r.table('domains').get(message['template_id']).run(conn))
                return True
        except ReqlTimeoutError:
            print(e)
            return False          
        except Exception as e:
            print(e)
            return False                                       
        print(response.state)
        return True

    def engine_is_alive(self):
        """
        Client function to call the rpc
        """
        try:
            response = self.stub.EngineIsAlive(engine_pb2.Empty())
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == engine_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.is_alive       
        
        

curr_client = EngineClient()

import time

''' ENGINE IS ALIVE '''
# ~ print(curr_client.engine_is_alive())

''' NEW DESKTOP CREATION '''
# ~ templates = curr_client.template_list()
# ~ t=templates[0]
# ~ curr_client.desktop_from_template({'desktop_id':'_admin_power','template_id':t})

''' NEW DESKTOP CREATION '''
# ~ templates = curr_client.template_list()
# ~ t=templates[0]
# ~ hardware = {'vcpus':3}
# ~ curr_client.desktop_from_template({'desktop_id':'_admin_power11','template_id':t,'hardware':hardware})

''' NEW TEMPLATE CREATION '''
desktops = curr_client.desktop_list()
d=desktops[0]
hardware = {'vcpus':3}
curr_client.template_from_desktop({'desktop_id':d,'template_id':'_admin_vamoooooasdfs','hardware':hardware})

''' TEST VIEWER '''
# ~ curr_client.desktop_stop('_admin_renew')
# ~ curr_client.desktop_start('_admin_renew')
# ~ curr_client.desktop_viewer('_admin_renew')

''' BULK CREATE DELETE '''
# ~ desktops = curr_client.desktop_list()
# ~ templates = curr_client.template_list()
# ~ t=templates[0]
# ~ for i in range(0,20):
    # ~ curr_client.desktop_from_template({'desktop_id':'_admin_pepinillo_'+str(i),'template_id':t})
    # ~ print('Created desktop: '+str(i))
# ~ for i in range(0,20):
    # ~ curr_client.desktop_delete('_admin_pepinillo_'+str(i))
    # ~ print('deleting desktop')
    
'''delete'''
# ~ desktops = curr_client.desktop_list()
# ~ print(desktops)
# ~ curr_client.desktop_delete(desktops[0])
# ~ desktops = curr_client.desktop_list()
# ~ print(desktops)

'''list'''
# ~ desktops = curr_client.desktop_list()
# ~ print(desktops)
# ~ print(curr_client.desktop_get(desktops[0]))
# ~ curr_client.desktop_get('_admin_downloaded_zxspectrum')

'''start/stop'''
# ~ while True:
    # ~ curr_client.desktop_start('_admin_downloaded_zxspectrum')
    # ~ # time.sleep(1)
    # ~ curr_client.desktop_stop('_admin_downloaded_zxspectrum')


# ~ curr_client.domain_delete('_admin_downloaded_tetros')


# ~ message = {'domain_id':'el id de nou domain','template_id':'el id de plantilla a derivar'}
# ~ curr_client.domain_create_from_id(message)
