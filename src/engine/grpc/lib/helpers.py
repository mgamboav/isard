
''' get viewer for desktop_id '''
def get_viewer(viewer):
    return {'hostname':viewer['hostname'],
            'hostname_external':viewer['hostname_external'],
            # ~ 'port':int(viewer['port']),
            # ~ 'port_tls':int(viewer['tlsport']),
            'port_spice':int(viewer['port_spice']),
            'port_spice_ssl':int(viewer['port_spice_ssl']),
            'port_vnc':int(viewer['port_vnc']),
            'port_vnc_websocket':int(viewer['port_vnc_websocket']),
            'passwd':viewer['passwd'],
            'client_addr':viewer['client_addr'] if viewer['client_addr'] else '',
            'client_since':viewer['client_since'] if viewer['client_since'] else 0.0}

def load_config():
        '''
        Read RethinkDB configuration from file
        '''
        import configparser
        import os
        import shutil
        if not os.path.isfile(os.path.join(os.path.join(os.path.dirname(__file__),'../../../isard.conf'))):
            try:
                print('isard.conf not found, trying to copy from isard.conf.default')
                shutil.copyfile('isard.conf.default', 'isard.conf') 
            except Exception as e:
                print('Aborting, isard.conf.default not found. Please configure your RethinkDB database in file isard.conf')
                print(str(e))
                return False

        try:
            rcfg = configparser.ConfigParser()
            rcfg.read(os.path.join(os.path.dirname(__file__),'../../../isard.conf'))
        except Exception as e:
            print('isard.conf file can not be opened. \n Exception load_config: {}'.format(e))
            return False
        hyper={}
        try:
            for key,val in dict(rcfg.items('DEFAULT_HYPERVISORS')).items():
                vals=val.split(',')
                hyper[key]={'id': key,
                            'hostname': vals[0],
                            'viewer_hostname': vals[1],
                            'user': vals[2],
                            'port': vals[3],
                            'capabilities': {'disk_operations': True if int(vals[4]) else False,
                                             'hypervisor': True if int(vals[5]) else False},
                            'hypervisors_pools': [vals[6]],
                            'enabled': True if int(vals[7]) else False}                                                     

            return {'RETHINKDB_HOST': rcfg.get('RETHINKDB', 'HOST'),
                    'RETHINKDB_PORT': rcfg.get('RETHINKDB', 'PORT'),
                    'RETHINKDB_DB':   rcfg.get('RETHINKDB', 'DBNAME'),
                    'LOG_LEVEL': rcfg.get('LOG', 'LEVEL'),
                    'LOG_FILE': rcfg.get('LOG', 'FILE'),
                    'DEFAULT_HYPERVISORS': hyper}
        except Exception as e:
            print('isard.conf file can not be opened. \n Exception: {}'.format(e))
            return False
