import threading
import grpc

# ~ import sys
# ~ sys.path.append("..")

from engine.exceptions import *
from api.grpc.proto import desktop_pb2
from api.grpc.proto import desktop_pb2_grpc
# ~ from engine.grpc.proto import desktops_stream_pb2
# ~ from engine.grpc.proto import desktops_stream_pb2_grpc
# ~ from engine.grpc.proto import template_pb2
# ~ from engine.grpc.proto import template_pb2_grpc
# ~ from engine.grpc.proto import templates_stream_pb2
# ~ from engine.grpc.proto import templates_stream_pb2_grpc
# ~ from engine.grpc.proto import template_pb2
# ~ from engine.grpc.proto import base_pb2_grpc
# ~ from engine.grpc.proto import bases_stream_pb2
# ~ from engine.grpc.proto import bases_stream_pb2_grpc
# ~ from engine.grpc.proto import media_pb2
# ~ from engine.grpc.proto import media_pb2_grpc
# ~ from engine.grpc.proto import media_stream_pb2_grpc
# ~ from engine.grpc.proto import engine_pb2
# ~ from engine.grpc.proto import engine_pb2_grpc

class EngineClient(object):
    """
    Client for accessing the gRPC functionality
    """
 
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 1313
 
        # instantiate a communication channel
        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.server_port))
 
        # bind the client to the server channel
        self.desktop_stub = desktop_pb2_grpc.DesktopStub(self.channel)
        # ~ self.desktops_stream_stub = desktops_stream_pb2_grpc.DesktopsStreamStub(self.channel)
        # ~ self.template_stub = template_pb2_grpc.TemplateStub(self.channel)
        # ~ self.templates_stream_stub = templates_stream_pb2_grpc.TemplatesStreamStub(self.channel)
        # ~ self.base_stub = base_pb2_grpc.BaseStub(self.channel)
        # ~ self.bases_stream_stub = bases_stream_pb2_grpc.BasesStreamStub(self.channel)
        # ~ self.media_stub = media_pb2_grpc.MediaStub(self.channel)
        # ~ self.media_stream_stub = media_stream_pb2_grpc.MediaStreamStub(self.channel)
        # ~ self.engine_stub = engine_pb2_grpc.EngineStub(self.channel)

    ''' DESKTOPS STREAM '''
    def desktops_changes(self):
        try:
            for c in self.desktops_stream_stub.Changes(desktops_stream_pb2.DesktopsStreamRequest()):
                print(c.state)
                print(c.viewer)
        except KeyboardInterrupt:            
            return 
            
    def desktop_get(self, message):
        """
        Client function to call the rpc
        """
        try:
            print('engine client: '+message)
            response = self.desktop_stub.Get(desktop_pb2.GetRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.desktop

# ~ 
    def desktop_list(self):
        """
        Client function to call the rpc
        """
        try:
            response = self.desktop_stub.List(desktop_pb2.ListRequest())
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.desktops
                 
    def desktop_start(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.desktop_stub.Start(desktop_pb2.StartRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        # ~ print(response.state)
        # ~ print(response.viewer)
        return True

    def desktop_viewer(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.desktop_stub.Viewer(desktop_pb2.ViewerRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStopResponse.State.STARTED:
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
            response = self.desktop_stub.Stop(desktop_pb2.StopRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStopResponse.State.STARTED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)
        # ~ print(response.state)
        return True

    def desktop_delete(self, message):
        """
        Client function to call the rpc
        """
        try:
            response = self.desktop_stub.Delete(desktop_pb2.DeleteRequest(desktop_id=message))
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStopResponse.State.STARTED:
            #~ print(message+' was stopped')
        #~ else:
            #~ print(response.state)
        print(response.state)
        return True

    # ~ def template_list(self):
        # ~ """
        # ~ Client function to call the rpc
        # ~ """
        # ~ try:
            # ~ response = self.desktop_stub.TemplateList(desktop_pb2.Empty())
        # ~ except grpc.RpcError as e:
            # ~ print(e.details())
            # ~ print(e.code().name)
            # ~ print(e.code().value)
            # ~ if grpc.StatusCode.INTERNAL == e.code():
                # ~ print('The error is internal')
            # ~ return False
                #~ if response.state == desktop_pb2.DesktopStartResponse.State.STARTED:
                    #~ print(message+' was started')
                #~ else:
                    #~ print(response.state)
        # ~ return response.templates
                        
    def desktop_from_template(self,message):
        """
        PARAMETERS: name, description, user, category, group, icon, server,
        os, options '''
        
        """
        try:
            if 'hardware' in message.keys():
                response = self.desktop_stub.FromTemplate(desktop_pb2.FromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id'], hardware=message['hardware']))
            else:
                response = self.desktop_stub.FromTemplate(desktop_pb2.FromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id']))
        except grpc.RpcError as e:
            ## Should be deleted as it failed?##
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopFromTemplateResponse.State.STOPPED:
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
                response = self.desktop_stub.TemplateFromDesktop(desktop_pb2.DesktopFromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id'], hardware=message['hardware']))
            else:
                response = self.desktop_stub.TemplateFromDesktop(desktop_pb2.DesktopFromTemplateRequest(desktop_id=message['desktop_id'], template_id=message['template_id']))
        except grpc.RpcError as e:
            ## Should be deleted as it failed?##
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopFromTemplateResponse.State.STOPPED:
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
            response = self.engine_stub.EngineIsAlive(engine_pb2.EngineIsAliveRequest())
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response.is_alive       

    def engine_status(self):
        """
        Client function to call the rpc
        """
        try:
            response = self.engine_stub.EngineStatus(engine_pb2.EngineStatusRequest())
        except grpc.RpcError as e:
            print(e.details())
            print(e.code().name)
            print(e.code().value)
            if grpc.StatusCode.INTERNAL == e.code():
                print('The error is internal')
            return False
        #~ if response.state == desktop_pb2.DesktopStartResponse.State.STARTED:
            #~ print(message+' was started')
        #~ else:
            #~ print(response.state)
        return response         
        

curr_client = EngineClient()

import time
# ~ ''' CHANGES '''
#threading.Thread(target=curr_client.desktops_changes, daemon=True).start()
#while True: time.sleep(9999)

# ~ curr_client.domain_changes()

print(curr_client.desktop_get('_admin_tetros1'))
''' ENGINE IS ALIVE '''
# ~ print(curr_client.engine_is_alive())
# ~ print(curr_client.engine_status())

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
# ~ desktops = curr_client.desktop_list()
# ~ d=desktops[0]
# ~ hardware = {'vcpus':3}
# ~ curr_client.template_from_desktop({'desktop_id':d,'template_id':'_admin_vamoooooasdfs','hardware':hardware})


''' LOKER START/STOP THREAD '''
# ~ j=20
# ~ while j<=20:
    # ~ i=1
    # ~ while i<=10:
        # ~ threading.Thread(target=curr_client.desktop_start, args=('_admin_tetros'+str(i),), daemon=False).start()
        # ~ i=i+1
    #time.sleep(10)

    # ~ i=1
    # ~ while i<=10:
        # ~ threading.Thread(target=curr_client.desktop_stop, args=('_admin_tetros'+str(i),), daemon=False).start()
        # ~ i=i+1
        
    # ~ j=j+1
    
    # ~ threading.Thread(target=curr_client.desktop_start, args=('_admin_downloaded_tetros',), daemon=False).start()
    # ~ threading.Thread(target=curr_client.desktop_start, args=('_admin_downloaded_zxspectrum',), daemon=False).start()

    # ~ threading.Thread(target=curr_client.desktop_stop, args=('_admin_downloaded_tetros',), daemon=False).start()
    # ~ threading.Thread(target=curr_client.desktop_stop, args=('_admin_downloaded_zxspectrum',), daemon=False).start()

''' TEST VIEWER '''        
# ~ print(curr_client.desktop_start('_admin_downloaded_tetros'))
# ~ print(curr_client.desktop_stop('_admin_downloaded_tetros'))
# ~ curr_client.desktop_viewer('_admin_downloaded_tetros')

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
# ~ print(curr_client.desktop_get('_admin_downloaded_zxspectrum'))

# ~ '''start/stop'''
# ~ while True:
    # ~ curr_client.desktop_start('_admin_downloaded_zxspectrum')
    # ~ # time.sleep(1)
    # ~ curr_client.desktop_stop('_admin_downloaded_zxspectrum')


# ~ curr_client.domain_delete('_admin_downloaded_tetros')


# ~ message = {'domain_id':'el id de nou domain','template_id':'el id de plantilla a derivar'}
# ~ curr_client.domain_create_from_id(message)
