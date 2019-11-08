XML_INTERFACE_NETWORK = {'name': 'network',
'xml': '''
    <interface type="network">
      <source network="{source}"/>
      <mac address="{mac}"/>
      <model type="{model}"/>
    </interface>
'''}

XML_INTERFACE_BRIDGE = {'name': 'bridge',
'xml': '''
    <interface type="bridge">
      <source bridge="{source}"/>
      <mac address="{mac}"/>
      <model type="{model}"/>
    </interface>
'''}

XML_MEDIA_CDROM = {'name': 'iso',
'xml': '''
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <source file="{source}"/>
      <target dev="hd{target_suffix}" bus="ide"/>
      <readonly/>
    </disk>
'''

XML_DISK = {'name': 'disk',
'xml': '''
    <disk type="file" device="disk">
      <driver name="qemu" type="{driver_type}"/>
      <source file="{source}"/>
      <target dev="{prefix_suffix}d{target_suffix}" bus="{bus}"/>
    </disk>
'''}

XML_DISK_READONLY = {'name': 'disk_readonly',
'xml': '''
    <disk type="file" device="disk">
      <driver name="qemu" type="{driver_type}"/>
      <source file="{source}"/>
      <target dev="{prefix_suffix}d{target_suffix}" bus="{bus}"/>
      <readonly/>
    </disk>
'''}

    <disk type="file" device="floppy">
      <driver name="qemu" type="raw"/>
      <source file="/home/tmp/floppy.img"/>
      <target dev="fda" bus="fdc"/>
    </disk>
    
        <graphics type="spice" port="-1" tlsPort="-1" autoport="yes">
      <image compression="off"/>
    </graphics>
    
    <video>
      <model type="qxl"/>
    </video>
    
    <sound model='ich6'>
      <codec type='micro'/>
    <sound/>
            
XML_DISK_DEVICE = {'name': 'disk_device',
'xml': '''
<disk type='block' device='disk'>
    <driver name='qemu' type='raw'/>
    <source dev='{source}'/>
    <target dev='vdb' bus='virtio'/>
</disk>
'''}

XML_MEMORY = {'NAME': 'memory',
'xml': '''
  <memory>2097152</memory>
  <currentMemory>2097152</currentMemory>
'''}
# ~ driver_type = qcow2, raw
# ~ bus = ide, sata, virtio, scsi




<domain type="kvm">
  <name>fedora26</name>
  <uuid>c8be35a9-59eb-4f43-86fb-f9002e046ed5</uuid>
  <memory>2097152</memory>
  <currentMemory>2097152</currentMemory>
  <vcpu>1</vcpu>
  <os>
    <type arch="x86_64">hvm</type>
    <boot dev="network"/>
    <boot dev="cdrom"/>
    <boot dev="fd"/>
    <boot dev="hd"/>
    <bootmenu enable="yes"/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <vmport state="off"/>
  </features>
  <cpu mode="custom" match="exact">
    <model>Haswell-noTSX</model>
  </cpu>
  <clock offset="utc">
    <timer name="rtc" tickpolicy="catchup"/>
    <timer name="pit" tickpolicy="delay"/>
    <timer name="hpet" present="no"/>
  </clock>
  <pm>
    <suspend-to-mem enabled="no"/>
    <suspend-to-disk enabled="no"/>
  </pm>
  <devices>
    <emulator>/usr/bin/qemu-kvm</emulator>
    <disk type="file" device="disk">
      <driver name="qemu" type="qcow2"/>
      <source file="/home/tmp/disk.qcow2"/>
      <target dev="vda" bus="virtio"/>
    </disk>
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <source file="/home/tmp/cdrom.iso"/>
      <target dev="hda" bus="ide"/>
      <readonly/>
    </disk>
    <disk type="file" device="floppy">
      <driver name="qemu" type="raw"/>
      <source file="/home/tmp/floppy.img"/>
      <target dev="fda" bus="fdc"/>
    </disk>
    <controller type="usb" index="0" model="ich9-ehci1"/>
    <controller type="usb" index="0" model="ich9-uhci1">
      <master startport="0"/>
    </controller>
    <controller type="usb" index="0" model="ich9-uhci2">
      <master startport="2"/>
    </controller>
    <controller type="usb" index="0" model="ich9-uhci3">
      <master startport="4"/>
    </controller>
    <interface type="bridge">
      <source bridge="br"/>
      <mac address="52:54:00:0e:ec:71"/>
      <model type="virtio"/>
    </interface>
    <input type="tablet" bus="usb"/>
    <graphics type="spice" port="-1" tlsPort="-1" autoport="yes">
      <image compression="off"/>
    </graphics>
    <console type="pty"/>
    <channel type="unix">
      <source mode="bind"/>
      <target type="virtio" name="org.qemu.guest_agent.0"/>
    </channel>
    <channel type="spicevmc">
      <target type="virtio" name="com.redhat.spice.0"/>
    </channel>
    <sound model="ich6"/>
    <video>
      <model type="qxl"/>
    </video>
    <redirdev bus="usb" type="spicevmc"/>
    <redirdev bus="usb" type="spicevmc"/>
    <rng model="virtio">
      <backend model="random">/dev/urandom</backend>
    </rng>
  </devices>
</domain>


