from sm.desktop_sm import DesktopSM, StateInvalidError
# ~ import engine.exceptions
from engine.exceptions import *
import random,time,string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class EngineMock():
    def __init__(self):
        self.desktop_sm = DesktopSM()
        self.db = create_engine('postgresql://isardvdi:isardvdi@isard-database:5432/engine')
        self.dbsession = sessionmaker(bind=self.db)
        self.mem = MemoryMock()
        self.db_desktops = {}
        viewer = {  'hostname': 'mock.local',
                    'hostname_external':'mock.com',
                    'tlsport': 5678,
                    'port': 5679,
                    'port_spice': 5901,
                    'port_spice_ssl': 5902,
                    'port_vnc': 6900,
                    'port_vnc_websocket': 6901,
                    'passwd': '87023ycn1034',
                    'client_addr': False,
                    'client_since': False}        

    def _rnd_string(self,n):
        return ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k = n)) 

    def _rdn_id(self):
        return '_'+_rnd_string(8)+'_'+_rnd_string(2)+'_'+_rnd_string(10)+'_'++_rnd_string(4)+'_'
                                        
    def DesktopGet(self,desktop_id):
        ''' From running dict '''
        desktop = self.db.select('desktops',desktop_id)
        if desktop is not None: return desktop
        raise NotFoundError(desktop_id, 'Desktop not found in system')
    
    def DesktopGetState(desktop_ids):
        return self.mem.desktops[destop_id]['state']
        
    def DesktopStart(desktop_id):
        try:
            # ~ next_actions = 
            if 'START' in self.desktop_sm.get_next_actions(self.desktops[desktop_id][state]):
                self.desktops[desktop_id][state]='STARTED'
                ''' XML WITH VIEWER IS RETURNED IN dom.createXML(). Needs parsing. '''

                return viewer
        except Exception as e:
            raise
    def DesktopFromTemplate(self,desktop_id,template_id,hardware):
        self.db.select_desktop(template_id)

        

class MemoryMock():    
    def __init():    
        self.desktops = {}

    def engine_status(self):
        return True
                
    def get_desktops(self):
        return self.desktops
        
    def get_viewer(self):
        return {  'hostname': 'mock.local',
                    'hostname_external':'mock.com',
                    'tlsport': 5678,
                    'port': 5679,
                    'port_spice': 5901,
                    'port_spice_ssl': 5902,
                    'port_vnc': 6900,
                    'port_vnc_websocket': 6901,
                    'passwd': '87023ycn1034',
                    'client_addr': False,
                    'client_since': False}     
