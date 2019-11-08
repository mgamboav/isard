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

XML_DISK_DEVICE = {'name': 'disk_device',
'xml': '''
<disk type='block' device='disk'>
    <driver name='qemu' type='raw'/>
    <source dev='{source}'/>
    <target dev='vdb' bus='virtio'/>
</disk>
'''}
# ~ driver_type = qcow2, raw
# ~ bus = ide, sata, virtio, scsi

