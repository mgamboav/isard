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
                    'video':[]}
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
      <target dev="hd{target_suffix}" bus="ide"/>
      <readonly/>
    </disk>
'''})

        snippets['disk'].append({'name': 'disk',
        'xml': '''
    <disk type="file" device="disk">
      <driver name="qemu" type="{driver_type}"/>
      <source file="{source}"/>
      <target dev="{prefix_suffix}d{target_suffix}" bus="{bus}"/>
    </disk>
'''})

        snippets['disk'].append({'name': 'disk_ro',
        'xml': '''
    <disk type="file" device="disk">
      <driver name="qemu" type="{driver_type}"/>
      <source file="{source}"/>
      <target dev="{prefix_suffix}d{target_suffix}" bus="{bus}"/>
      <readonly/>
    </disk>
'''})

        snippets['media'].append({'name': 'floppy',
        'xml': '''
    <disk type="file" device="floppy">
      <driver name="qemu" type="raw"/>
      <source file="{source}"/>
      <target dev="{prefix_suffix}d{target_suffix}" bus="fdc"/>
    </disk>
'''})

        snippets['media'].append({'name': 'floppy_ro',
        'xml': '''
    <disk type="file" device="floppy">
      <driver name="qemu" type="raw"/>
      <source file="{source}"/>
      <target dev="{prefix_suffix}d{target_suffix}" bus="fdc"/>
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

# ~ <graphics type='spice' port='-1' tlsPort='-1' autoport='yes'>
  # ~ <channel name='main' mode='secure'/>
  # ~ <channel name='record' mode='insecure'/>
  # ~ <image compression='auto_glz'/>
  # ~ <streaming mode='filter'/>
  # ~ <clipboard copypaste='no'/>
  # ~ <mouse mode='client'/>
  # ~ <filetransfer enable='no'/>
  # ~ <gl enable='yes' rendernode='/dev/dri/by-path/pci-0000:00:02.0-render'/>
# ~ </graphics>

        return snippets[kind]
        
    # ~ <disk type="file" device="floppy">
      # ~ <driver name="qemu" type="raw"/>
      # ~ <source file="/home/tmp/floppy.img"/>
      # ~ <target dev="fda" bus="fdc"/>
    # ~ </disk>
    
        # ~ <graphics type="spice" port="-1" tlsPort="-1" autoport="yes">
      # ~ <image compression="off"/>
    # ~ </graphics>
    
    # ~ <video>
      # ~ <model type="qxl"/>
    # ~ </video>
    
    # ~ <sound model='ich6'>
      # ~ <codec type='micro'/>
    # ~ <sound/>
            

# ~ XML_MEMORY = {'NAME': 'memory',
# ~ 'xml': '''
  # ~ <memory>{memory}</memory>
  # ~ <currentMemory>{current_memory}</currentMemory>
# ~ '''}
# ~ driver_type = qcow2, raw
# ~ bus = ide, sata, virtio, scsi

# ~ <domain type="kvm">
  # ~ <name>fedora26</name>
  # ~ <uuid>c8be35a9-59eb-4f43-86fb-f9002e046ed5</uuid>
  # ~ <memory>2097152</memory>
  # ~ <currentMemory>2097152</currentMemory>
  # ~ <vcpu>1</vcpu>
  # ~ <os>
    # ~ <type arch="x86_64">hvm</type>
    # ~ <boot dev="network"/>
    # ~ <boot dev="cdrom"/>
    # ~ <boot dev="fd"/>
    # ~ <boot dev="hd"/>
    # ~ <bootmenu enable="yes"/>
  # ~ </os>
  # ~ <features>
    # ~ <acpi/>
    # ~ <apic/>
    # ~ <vmport state="off"/>
  # ~ </features>
  # ~ <cpu mode="custom" match="exact">
    # ~ <model>Haswell-noTSX</model>
  # ~ </cpu>
  # ~ <clock offset="utc">
    # ~ <timer name="rtc" tickpolicy="catchup"/>
    # ~ <timer name="pit" tickpolicy="delay"/>
    # ~ <timer name="hpet" present="no"/>
  # ~ </clock>
  # ~ <pm>
    # ~ <suspend-to-mem enabled="no"/>
    # ~ <suspend-to-disk enabled="no"/>
  # ~ </pm>
  # ~ <devices>
    # ~ <emulator>/usr/bin/qemu-kvm</emulator>
    # ~ <disk type="file" device="disk">
      # ~ <driver name="qemu" type="qcow2"/>
      # ~ <source file="/home/tmp/disk.qcow2"/>
      # ~ <target dev="vda" bus="virtio"/>
    # ~ </disk>
    # ~ <disk type="file" device="cdrom">
      # ~ <driver name="qemu" type="raw"/>
      # ~ <source file="/home/tmp/cdrom.iso"/>
      # ~ <target dev="hda" bus="ide"/>
      # ~ <readonly/>
    # ~ </disk>
    # ~ <disk type="file" device="floppy">
      # ~ <driver name="qemu" type="raw"/>
      # ~ <source file="/home/tmp/floppy.img"/>
      # ~ <target dev="fda" bus="fdc"/>
    # ~ </disk>
    # ~ <controller type="usb" index="0" model="ich9-ehci1"/>
    # ~ <controller type="usb" index="0" model="ich9-uhci1">
      # ~ <master startport="0"/>
    # ~ </controller>
    # ~ <controller type="usb" index="0" model="ich9-uhci2">
      # ~ <master startport="2"/>
    # ~ </controller>
    # ~ <controller type="usb" index="0" model="ich9-uhci3">
      # ~ <master startport="4"/>
    # ~ </controller>
    # ~ <interface type="bridge">
      # ~ <source bridge="br"/>
      # ~ <mac address="52:54:00:0e:ec:71"/>
      # ~ <model type="virtio"/>
    # ~ </interface>
    # ~ <input type="tablet" bus="usb"/>
    # ~ <graphics type="spice" port="-1" tlsPort="-1" autoport="yes">
      # ~ <image compression="off"/>
    # ~ </graphics>
    # ~ <console type="pty"/>
    # ~ <channel type="unix">
      # ~ <source mode="bind"/>
      # ~ <target type="virtio" name="org.qemu.guest_agent.0"/>
    # ~ </channel>
    # ~ <channel type="spicevmc">
      # ~ <target type="virtio" name="com.redhat.spice.0"/>
    # ~ </channel>
    # ~ <sound model="ich6"/>
    # ~ <video>
      # ~ <model type="qxl"/>
    # ~ </video>
    # ~ <redirdev bus="usb" type="spicevmc"/>
    # ~ <redirdev bus="usb" type="spicevmc"/>
    # ~ <rng model="virtio">
      # ~ <backend model="random">/dev/urandom</backend>
    # ~ </rng>
  # ~ </devices>
# ~ </domain>


