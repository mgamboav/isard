
''' get viewer for desktop_id '''
def get_viewer(viewer):
    try:
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
    except Exception as e:
        print(str(e))
        return {}
