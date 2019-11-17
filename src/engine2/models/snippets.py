from os import path, getcwd
from os import listdir
from os.path import isfile, join

class XMLHelper(object):
    def __init__(object):
        pass
        
    def get_virtinstalls(self):
        # ~ __location__ = path.realpath(
                        # ~ path.join(getcwd(), path.dirname(__file__)))
        kinds=['virt-install','custom']
        # ~ paths=['models/xmls/virt-install.lst','./xml/custom.lst']
        installs=[]
        for k in kinds:
            f=open('models/xmls/'+k+'.lst')
            data = f.read()
            f.close()
            for l in data.split('\n')[2:]:
                if l.find('|') > 1:
                    v=[a.strip() for a in l.split('|')]
                    xml=self._get_virtinstall_xml(k,v[0])
                    if xml is not False:
                        # ~ icon=self.get_icon(v[1])               
                        installs.append({'name':v[0].strip(),
                                         # ~ 'name':v[1].strip(),
                                         # ~ 'vers':v[2].strip(),
                                         # ~ 'www':v[3].strip(),
                                         # ~ 'icon':icon,
                                         'xml':xml})

        #~ import pprint
        #~ pprint.pprint(installs)
        return installs

    def _get_virtinstall_xml(self,kind,id):
        try:
            f=open('models/xmls/virt-install/'+id+'.xml')
            data = f.read()
            f.close()
        except:
            return False
        return data        

    def get_snippets(self,kind):
        snippets={'interface':[],
                    'disk':[],
                    'media':[],
                    'graphic':[],
                    'video':[],
                    'memory':[],
                    'vcpu':[],
                    'cpu':[],
                    'sound':[]}
        snippets['interface'].append({'name': 'network',
        'xml': '''
    <interface type="network">
      <source network="{source}"/>
      <mac address="{mac}"/>
      <model type="{model}"/>
    </interface>
'''})

        snippets['interface'].append({'name': 'bridge',
        'xml': '''
    <interface type="bridge">
      <source bridge="{source}"/>
      <mac address="{mac}"/>
      <model type="{model}"/>
    </interface>
'''})

        snippets['media'].append({'name': 'iso',
        'xml': '''
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <source file="{source}"/>
      <target dev="{dev}" bus="ide"/>
      <readonly/>
    </disk>
'''})

        snippets['disk'].append({'name': 'disk',
        'xml': '''
    <disk type="file" device="disk">
      <driver name="qemu" type="{format}"/>
      <source file="{source}"/>
      <target dev="{dev}" bus="{bus}"/>
    </disk>
'''})

        snippets['disk'].append({'name': 'disk_ro',
        'xml': '''
    <disk type="file" device="disk">
      <driver name="qemu" type="{driver_type}"/>
      <source file="{source}"/>
      <target dev="{dev}" bus="{bus}"/>
      <readonly/>
    </disk>
'''})

        snippets['media'].append({'name': 'floppy',
        'xml': '''
    <disk type="file" device="floppy">
      <driver name="qemu" type="raw"/>
      <source file="{source}"/>
      <target dev="{dev}" bus="fdc"/>
    </disk>
'''})

        snippets['media'].append({'name': 'floppy_ro',
        'xml': '''
    <disk type="file" device="floppy">
      <driver name="qemu" type="raw"/>
      <source file="{source}"/>
      <target dev="{dev}" bus="fdc"/>
      <readonly/>
    </disk>
'''})

        snippets['graphic'].append({'name': 'spice',
        'xml': '''
    <graphics type="spice" port="-1" tlsPort="-1" autoport="yes">
      <image compression="off"/>
    </graphics>
'''})

        snippets['video'].append({'name': 'qxl',
        'xml': '''
    <video>
      <model type="qxl"/>
    </video>
'''})

        # ~ snippets['memory'].append({'name': 'hotplug',
        # ~ 'xml': '''
  # ~ <maxMemory slots="{slots}" unit="{unit}">{maxmemory}</maxMemory>
  # ~ <memory unit="{unit}">{memory}</memory>
  # ~ <currentMemory unit="{unit}">{currentmemory}</currentMemory>
# ~ '''})

        snippets['memory'].append({'name': 'balloon',
        'xml': '''
  <memory unit="{unit}">{memory}</memory>
  <currentMemory unit="{unit}">{currentmemory}</currentMemory>
'''})

        snippets['vcpu'].append({'name': 'vcpu',
        'xml': '''
  <vcpu>{vcpu}</vcpu>
'''})

        snippets['cpu'].append({'name': 'host_passthrough',
        'xml': '''
  <cpu mode="host-passthrough">
  </cpu>
'''})

  # ~ <cpu mode='host-model' check='partial'>
    # ~ <model fallback='allow'/>
  # ~ </cpu>

        snippets['cpu'].append({'name': 'host_model',
        'xml': '''
  <cpu mode="host-model" check="partial">
    <model fallback="{fallback}"/>
  </cpu>
'''})

        snippets['cpu'].append({'name': 'custom',
        'xml': '''
  <cpu mode="custom" match="{match}">
    <model fallback="{fallback}">{model}</model>
  </cpu>
'''})

        snippets['sound'].append({'name': 'ich6',
        'xml': '''
  <sound model="ich6"/>
'''})

        return snippets[kind]
