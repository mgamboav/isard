from common.sm.desktop_sm import DesktopSM
# ~ import engine.exceptions
from common.exceptions.engine import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.desktop import *
from api.grpc.proto import desktop_pb2
import sys, os

class EngineMock(object):
    def __init__(self):
        self.desktop_sm = DesktopSM()
        
        self.db = create_engine('postgresql://isardvdi:isardvdi@isard-database:5432/engine')
        self.dbsession = sessionmaker(bind=self.db)
        self.session = self.dbsession()
        self.desktop = DesktopMock(self.session)

class DesktopMock(object):
    def __init__(self, session):
        self.session = session    
            
    def video_list(self,pb=False):
        ''' From running dict '''
        try:
            videos = self.session.query(Video).all()
            if pb:
                return [desktop_pb2.Video(**v.to_dict()) for v in videos]
            videos_dict = {}
            for video in [v.to_dict() for v in videos]:
                id = video.pop('id')
                videos_dict[id] = video
            return videos_dict
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

    def boot_list(self,pb=False):
        ''' From running dict '''
        try:
            boots = self.session.query(Boot).all()
            if pb:
                return [desktop_pb2.Boot(**b.to_dict()) for b in boots]
            boots_dict = {}
            for boot in [b.to_dict() for b in boots]:
                id = boot.pop('id')
                boots_dict[id] = boot
            return boots_dict
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

    def disk_bus_list(self,pb=False):
        ''' From running dict '''
        try:
            disk_buses = self.session.query(Boot).all()
            if pb:
                return [desktop_pb2.DiskBus(**b.to_dict()) for b in disk_buses]
            disk_buses_dict = {}
            for disk_bus in [db.to_dict() for db in disk_buses]:
                id = disk_bus.pop('id')
                disk_buses_dict[id] = disk_bus
            return disk_buses_dict
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

    def disk_format_list(self,pb=False):
        ''' From running dict '''
        try:
            disk_formats = self.session.query(DiskFormat).all()
            if pb:
                return [desktop_pb2.DiskFormat(**df.to_dict()) for df in disk_formats]
            disk_formats_dict = {}
            for disk_format in [df.to_dict() for df in disk_formats]:
                id = disk_format.pop('id')
                disk_formats_dict[id] = disk_format
            return disk_formats_dict
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

    def graphic_list(self,pb=False):
        ''' From running dict '''
        try:
            graphics = self.session.query(Graphic).all()
            if pb:
                return [desktop_pb2.Graphic(**g.to_dict()) for g in graphics]
            graphics_dict = {}
            for graphic in [g.to_dict() for g in graphics]:
                id = graphic.pop('id')
                graphics_dict[id] = graphic
            return graphics_dict
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

    def interface_list(self,pb=False):
        ''' From running dict '''
        try:
            interfaces = self.session.query(Interface).all()
            if pb:
                return [desktop_pb2.Interface(**i.to_dict()) for i in interfaces]
            interfaces_dict = {}
            for interface in [i.to_dict() for i in interfaces]:
                id = interface.pop('id')
                interfaces_dict[id] = interface
            return interfaces_dict
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')

    # ~ def from_template(self, desktop_id, template_id, hardware, pb=False):
        # ~ ''' '''
        # ~ try:
            # ~ boots = [Boot(b) for b in hardware['boots']
            # ~ result = self.session.query(Interface).all()
            # ~ if pb:
                # ~ return [desktop_pb2.Interface(**i.to_dict()) for i in interfaces]
            # ~ interfaces_dict = {}
            # ~ for interface in [i.to_dict() for i in interfaces]:
                # ~ id = interface.pop('id')
                # ~ interfaces_dict[id] = interface
            # ~ return interfaces_dict
        # ~ except Exception as e:
            # ~ exc_type, exc_obj, exc_tb = sys.exc_info()
            # ~ fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ~ raise Exception(f'boot_list error: \nType: {exc_type}\n File: {fname}\n Line: {exc_tb.tb_lineno}\n Error: {e}')                                                                                              
    # ~ def DesktopGet(self,desktop_id):
        # ~ ''' From running dict '''
        # ~ desktop = self.db.select('desktops',desktop_id)
        # ~ if desktop is not None: return desktop
        # ~ raise NotFoundError(desktop_id, 'Desktop not found in system')
    
    # ~ def DesktopGetState(desktop_ids):
        # ~ return self.mem.desktops[destop_id]['state']
        
    # ~ def DesktopStart(desktop_id):
        # ~ try:
           #next_actions = 
            # ~ if 'START' in self.desktop_sm.get_next_actions(self.desktops[desktop_id][state]):
                # ~ self.desktops[desktop_id][state]='STARTED'
                # ~ ''' XML WITH VIEWER IS RETURNED IN dom.createXML(). Needs parsing. '''

                # ~ return viewer
        # ~ except Exception as e:
            # ~ raise
    # ~ def DesktopFromTemplate(self,desktop_id,template_id,hardware):
        # ~ self.db.select_desktop(template_id)

    # ~ def _rnd_string(self,n):
        # ~ return ''.join(random.choices(string.ascii_uppercase +
                                     # ~ string.digits, k = n)) 

    # ~ def _rdn_id(self):
        # ~ viewer = {  'hostname': 'mock.local',
                    # ~ 'hostname_external':'mock.com',
                    # ~ 'tlsport': 5678,
                    # ~ 'port': 5679,
                    # ~ 'port_spice': 5901,
                    # ~ 'port_spice_ssl': 5902,
                    # ~ 'port_vnc': 6900,
                    # ~ 'port_vnc_websocket': 6901,
                    # ~ 'passwd': '87023ycn1034',
                    # ~ 'client_addr': False,
                    # ~ 'client_since': False}          
        # ~ return '_'+_rnd_string(8)+'_'+_rnd_string(2)+'_'+_rnd_string(10)+'_'++_rnd_string(4)+'_'        

# ~ class MemoryMock(object):    
    # ~ def __init(self,session):    
        # ~ self.session = session
        # ~ self.videos = []
        # ~ self.boots

    # ~ def static_data(self):
        # ~ videos = self.session.query(Video).all()
        # ~ self.videos = [**v.to_dict() for v in videos]  
        # ~ boots = self.session.query(Boot).all()
        # ~ self.boots = [**b.to_dict() for b in boots] 
        # ~ disk_buses = self.session.query(DiskBus).all()
        # ~ self.disk_buses = [**db.to_dict() for db in disk_buses] 
        # ~ disk_formats = self.session.query(DiskFormat).all()
        # ~ self.disk_formats = [**df.to_dict() for df in disk_formats] 
        # ~ graphics = self.session.query(Graphic).all()
        # ~ self.graphics = [**g.to_dict() for g in graphics]   
        # ~ interfaces = self.session.query(Interface).all()
        # ~ self.interfaces = [**i.to_dict() for i in interfaces]                                           

    # ~ def engine_status(self):
        # ~ return True

    
    # ~ def get_desktops(self):
        # ~ return self.desktops
        
    # ~ def get_viewer(self):
        # ~ return {  'hostname': 'mock.local',
                    # ~ 'hostname_external':'mock.com',
                    # ~ 'tlsport': 5678,
                    # ~ 'port': 5679,
                    # ~ 'port_spice': 5901,
                    # ~ 'port_spice_ssl': 5902,
                    # ~ 'port_vnc': 6900,
                    # ~ 'port_vnc_websocket': 6901,
                    # ~ 'passwd': '87023ycn1034',
                    # ~ 'client_addr': False,
                    # ~ 'client_since': False}     
