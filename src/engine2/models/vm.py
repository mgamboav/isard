import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.orderinglist import ordering_list

from models import db, Base
from models.base_mixin import BaseMixin

from models.parser.xml_parser import XmlParser

def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)
    return default_function

# ~ def get_all_data(vm_id,IntermediateObject, RelatedObject):
        # ~ relateds_table = db.query(IntermediateObject).filter(IntermediateObject.vm_id == vm_id).all()
        # ~ related_list = []
        # ~ for related_table in relateds_table:
            # ~ row = db.query(RelatedObject).filter(RelatedObject.id == related_table.media_id).first()
            # ~ related_list.append({**row._as_dict(), **related_table._as_dict()})
        # ~ return related_list
        
# ~ def file_name():
    # ~ def default_function(context):
        # ~ return context.current_parameters.get('name')+'.'+context.current_parameters.get('format')
    # ~ return default_function
    
class Vm_Sound(BaseMixin, Base):
    __tablename__ = 'vm_sound'

    __table_args__ = (
            sa.UniqueConstraint("vm_id", "sound_id"),
        )
        
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    sound_id = sa.Column(sa.Integer, sa.ForeignKey('sound_xml.id'), primary_key=True)
    
    sounds = relationship("SoundXML", back_populates="vm")
    vm = relationship("Vm", back_populates="sounds")

class Vm_Cpu(BaseMixin, Base):
    __tablename__ = 'vm_cpu'
        
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    cpu_id = sa.Column(sa.Integer, sa.ForeignKey('cpu_xml.id')) #, primary_key=True)
    match = sa.Column(sa.String, default='exact')
    fallback = sa.Column(sa.String, default='allow')
    model = sa.Column(sa.String, default='Haswell-noTSX')
    check = sa.Column(sa.String, default='partial')
    
    cpu = relationship("CpuXML", back_populates="vm")
    vm = relationship("Vm", back_populates="cpu")
            
class Vm_Vcpu(BaseMixin, Base):
    __tablename__ = 'vm_vcpu'

    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("vm_id", "vcpu_id"),
        # ~ )
        
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    vcpu_id = sa.Column(sa.Integer, sa.ForeignKey('vcpu_xml.id')) #, primary_key=True)
    vcpus = sa.Column(sa.Integer, nullable=False)
    
    vcpu = relationship("VcpuXML", back_populates="vm")
    vm = relationship("Vm", back_populates="vcpu")
    
class Vm_Memory(BaseMixin, Base):
    __tablename__ = 'vm_memory'

    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("vm_id", "memory_id"),
        # ~ )
        
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    memory_id = sa.Column(sa.Integer, sa.ForeignKey('memory_xml.id')) #, primary_key=True)
    unit = sa.Column(sa.String, default='MiB')
    mem = sa.Column(sa.Integer, nullable=False)
    maxmemory = sa.Column(sa.Integer, default=same_as('mem'))
    currentmemory = sa.Column(sa.Integer, default=same_as('mem'))
    
    memory = relationship("MemoryXML", back_populates="vm")
    vm = relationship("Vm", back_populates="memory")

    # ~ def _as_dict_(self):
        # ~ return {'memory':self.mem,'maxmemory':self.maxmemory,'currentmemory':self.currentmemory,'unit':self.unit}
                    
class Vm_Media(BaseMixin, Base):
    __tablename__ = 'vm_media'

    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    media_id = sa.Column(sa.Integer, sa.ForeignKey('media_xml.id'), primary_key=True)
    ppath = sa.Column(sa.String, default="disks/")
    rpath = sa.Column(sa.String, default="vms/")
    filename = sa.Column(sa.String, nullable=False)
    bus = sa.Column(sa.String, default="ide")
    format = sa.Column(sa.String, default="raw")
    order = sa.Column(sa.Integer, nullable=False)
    
    medias = relationship("MediaXML", back_populates="vms")
    vm = relationship("Vm", back_populates="medias")

class Vm_Interface(BaseMixin, Base):
    __tablename__ = 'vm_interface'
        
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id')) #, primary_key=True)
    interface_id = sa.Column(sa.Integer, sa.ForeignKey('interface_xml.id')) #, primary_key=True)
    order = sa.Column(sa.Integer, nullable=False)
    source = sa.Column(sa.String, default='default')
    model = sa.Column(sa.String, default='virtio')
    mac = sa.Column(sa.String) 

    __table_args__ = (
            sa.PrimaryKeyConstraint(vm_id, order),
        ) 
                    
    interfaces = relationship("InterfaceXML", back_populates="vms")
    vms = relationship("Vm", back_populates="interfaces")

class Vm_Graphic(BaseMixin, Base):
    __tablename__ = 'vm_graphic'

    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    graphic_id = sa.Column(sa.Integer, sa.ForeignKey('graphic_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer, nullable=False)
    
    graphics = relationship("GraphicXML", back_populates="vm")
    vm = relationship("Vm", back_populates="graphics")
        
class Vm_Video(BaseMixin, Base):
    __tablename__ = 'vm_video'

    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), primary_key=True)
    video_id = sa.Column(sa.Integer, sa.ForeignKey('video_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer, nullable=False)
    
    videos = relationship("VideoXML", back_populates="vms")
    vm = relationship("Vm", back_populates="videos")
      
class Vm(BaseMixin, Base):
    __tablename__ = 'vm'


    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    state = sa.Column(sa.String, default='STATE_UNIDENTIFIED')
    
    vm_xml_id = sa.Column(sa.Integer, sa.ForeignKey('vm_xml.id'), nullable=False)
    vm_xml = relationship("VmXML")  
    memory = relationship("Vm_Memory", 
                                        back_populates="vm") 
    vcpu = relationship("Vm_Vcpu", 
                                        back_populates="vm")                                         
    cpu = relationship("Vm_Cpu", 
                                        back_populates="vm")     
    boots = relationship("Boot", order_by="Boot.order",
                            collection_class=ordering_list('order'),
                            cascade="all, delete-orphan")
                                
    disks = relationship('Disk', order_by="Disk.order",
                            collection_class=ordering_list('order'),
                            cascade="all, delete-orphan")
    medias = relationship("Vm_Media", 
                                        back_populates="vm")
    graphics = relationship("Vm_Graphic", 
                                        back_populates="vm")
    interfaces = relationship("Vm_Interface", 
                                        back_populates="vms")                                                                                                                                                                                                                                                
    videos = relationship("Vm_Video", 
                                        back_populates="vm") 
    sounds = relationship("Vm_Sound", 
                                        back_populates="vm") 
  
                                        
 
    kind = sa.Column(sa.String)
    
    __mapper_args__ = {
        'polymorphic_on':kind,
        'polymorphic_identity':'vm'
    }
        
    def get_xml(vm_name):
        try:
            vm = Vm.by_name(vm_name)
            vm_tree = XmlParser(db.query(VmXML).filter(VmXML.id == vm.vm_xml_id).first().xml)
            vm_tree.vm_name_update(vm.name)
            vm_tree.vm_memory_update(MemoryXML.get_vm_memory(vm.id))
            vm_tree.vm_vcpu_update(VcpuXML.get_vm_vcpu(vm.id))
            vm_tree.vm_cpu_update(CpuXML.get_vm_cpu(vm.id))
            vm_tree.vm_boot_update([boot.name for boot in Boot.list(vm.name)])
            vm_tree.vm_sound_add(SoundXML.get_vm_sound(vm.id))
            for disk in Disk.get_vm_disks(vm.id):
                vm_tree.vm_disk_add(disk)
            for media in MediaXML.get_vm_medias(vm.id):
                vm_tree.vm_disk_add(media)
            for interface in InterfaceXML.get_vm_interfaces(vm.id):
                vm_tree.vm_interface_add(interface)         
            for graphic in GraphicXML.get_vm_graphics(vm.id):
                vm_tree.vm_graphic_add(graphic)  
            for video in VideoXML.get_vm_video(vm.id):
                vm_tree.vm_graphic_add(video) 
            return vm_tree.to_xml()

        except Exception as e:
            raise

    def get(self):
        # ~ vm = db.query(Vm).get(id)
        return {'id':self.id,'name':self.name,'state':self.state}

    def get_hardware(self):
        return {'memory': self.memory[0]._as_dict(),
				'vcpu': self.vcpu[0]._as_dict(),
				'cpu': self.cpu[0]._as_dict(),
				'boots': [boot._as_dict() for boot in self.boots],
				'disks': [disk._as_dict() for disk in self.disks],
				'medias': [media._as_dict() for media in self.medias],
				'interfaces': [interface._as_dict() for interface in self.interfaces],
				'graphics': [graphic._as_dict() for graphic in self.graphics],
				'videos': [video._as_dict() for video in self.videos],
				'sounds': [sound._as_dict() for sound in self.sounds]}
                            
class Disk(BaseMixin, Base):
    __tablename__ = 'disk'
    
    __table_args__ = (
            sa.UniqueConstraint("vm_id", "order"),
        )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    order = sa.Column(sa.Integer, nullable=False)
    
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id')) 
    
    xml_id = sa.Column(sa.Integer, sa.ForeignKey('disk_xml.id'), nullable=False)  
    xml = relationship('DiskXML')
    
    ppath = sa.Column(sa.String, default="disks/")
    rpath = sa.Column(sa.String, default="vms/")
    filename = sa.Column(sa.String, nullable=False)
    
    bus = sa.Column(sa.String, default='virtio')
    size = sa.Column(sa.Integer, default=10)
    format = sa.Column(sa.String, default='qcow2')

    # ~ def __init__(self, vm_id, name, xml, ppath="/", rpath=".",bus="virtio", dev="vda", size=5, format="qcow2", order=1):
        # ~ self.name = name
        # ~ self.xml = xml
        # ~ self.vm_id = vm_id
        # ~ self.ppath = ppath
        # ~ self.rpath = rpath
        # ~ self.bus = bus
        # ~ self.dev = dev
        # ~ self.size = size
        # ~ self.format = format  
        # ~ self.order = order  

    def get_vm_disks(vm_id):
        disks = db.query(Disk).filter(Disk.id == vm_id).all()
        disks_list = []
        for disk in disks:
            disks_list.append({'name':disk.name,
                            'xml': db.query(DiskXML).filter(DiskXML.id == disk.xml_id).first().xml,
                            'ppath': disk.ppath,
                            'rpath': disk.rpath,
                            'filename': disk.filename,
                            'bus': disk.bus,
                            'size': disk.size,
                            'format': disk.format,
                            'order': disk.order})
        return disks_list

class SoundXML(BaseMixin, Base):
    __tablename__ = 'sound_xml'
    
    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("vm_id"),
        # ~ )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    xml = sa.Column(sa.String, unique=True)

    vm = relationship("Vm_Sound", 
                                        back_populates="sounds")      

    def get_vm_sound(vm_id):
        vm_sound = db.query(Vm_Sound).filter(Vm_Sound.vm_id == vm_id).first()
        if vm_sound == None: return False
        sound = db.query(SoundXML).filter(SoundXML.id == vm_sound.sound_id).first()
        return {**sound._as_dict(), **vm_sound._as_dict()}
        
class MemoryXML(BaseMixin, Base):
    __tablename__ = 'memory_xml'
    
    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("vm_id"),
        # ~ )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    xml = sa.Column(sa.String, unique=True)

    vm = relationship("Vm_Memory", 
                                        back_populates="memory")      

    def get_vm_memory(vm_id):
        vm_memory = db.query(Vm_Memory).filter(Vm_Memory.vm_id == vm_id).first()
        memory = db.query(MemoryXML).filter(MemoryXML.id == vm_memory.memory_id).first()
        dict = {**memory._as_dict(), **vm_memory._as_dict()}
        dict['memory'] = dict.pop('mem')
        return dict
        
class CpuXML(BaseMixin, Base):
    __tablename__ = 'cpu_xml'
    
    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("vm_id"),
        # ~ )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    xml = sa.Column(sa.String, unique=True)

    vm = relationship("Vm_Cpu", 
                                        back_populates="cpu")  

    def get_vm_cpu(vm_id):
        vm_cpu = db.query(Vm_Cpu).filter(Vm_Cpu.vm_id == vm_id).first()
        cpu = db.query(CpuXML).filter(CpuXML.id == vm_cpu.cpu_id).first()
        return {**cpu._as_dict(), **vm_cpu._as_dict()}
                        
class VcpuXML(BaseMixin, Base):
    __tablename__ = 'vcpu_xml'
    
    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("vm_id"),
        # ~ )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    xml = sa.Column(sa.String, unique=True)

    vm = relationship("Vm_Vcpu", 
                                        back_populates="vcpu")  
    # ~ vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id')) 

    def get_vm_vcpu(vm_id):
        vm_vcpu = db.query(Vm_Vcpu).filter(Vm_Vcpu.vm_id == vm_id).first()
        vcpu = db.query(VcpuXML).filter(VcpuXML.id == vm_vcpu.vcpu_id).first()
        return {**vcpu._as_dict(), **vm_vcpu._as_dict()}
                        
class DiskXML(BaseMixin, Base):
    __tablename__ = "disk_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)

class VmXML(BaseMixin, Base):
    __tablename__ = "vm_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)

class MediaXML(BaseMixin, Base):
    __tablename__ = "media_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    vms = relationship("Vm_Media", 
                                        back_populates="medias")      

    def get_vm_medias(vm_id):
        vm_medias = db.query(Vm_Media).filter(Vm_Media.vm_id == vm_id).all()
        medias_list = []
        for vm_media in vm_medias:
            media = db.query(MediaXML).filter(MediaXML.id == vm_media.media_id).first()
            medias_list.append({**media._as_dict(), **vm_media._as_dict()})
        return medias_list         

class GraphicXML(BaseMixin, Base):
    __tablename__ = "graphic_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    vm = relationship("Vm_Graphic", 
                                        back_populates="graphics")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

    def get_vm_graphics(vm_id):
        vm_graphics = db.query(Vm_Graphic).filter(Vm_Graphic.vm_id == vm_id).all()
        graphics_list = []
        for vm_graphic in vm_graphics:
            graphic = db.query(GraphicXML).filter(GraphicXML.id == vm_graphic.graphic_id).first()
            graphics_list.append({**graphic._as_dict(), **vm_graphic._as_dict()})
        return graphics_list    
        
class VideoXML(BaseMixin, Base):
    __tablename__ = "video_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    vms = relationship("Vm_Video", 
                                        back_populates="videos")      

    def get_vm_video(vm_id):
        vm_videos = db.query(Vm_Video).filter(Vm_Video.vm_id == vm_id).all()
        videos_list = []
        for vm_video in vm_videos:
            video = db.query(VideoXML).filter(VideoXML.id == vm_video.video_id).first()
            videos_list.append({**video._as_dict(), **vm_video._as_dict()})
        return videos_list  
        
class InterfaceXML(BaseMixin, Base):
    __tablename__ = "interface_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    vms = relationship("Vm_Interface", 
                                        back_populates="interfaces")      

    def get_vm_interfaces(vm_id):
        vm_interfaces = db.query(Vm_Interface).filter(Vm_Interface.vm_id == vm_id).all()
        interfaces_list = []
        for vm_interface in vm_interfaces:
            interface = db.query(InterfaceXML).filter(InterfaceXML.id == vm_interface.interface_id).first()
            interfaces_list.append({**interface._as_dict(), **vm_interface._as_dict()})
        return interfaces_list  

class Boot(BaseMixin, Base):
    __tablename__ = "boot"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    vm_id = sa.Column(sa.Integer, sa.ForeignKey('vm.id'), nullable=False)
    order = sa.Column(sa.Integer, nullable=False)

    __table_args__ = (
            sa.UniqueConstraint(vm_id, name),
        )   
    # ~ __table_args__ = (
            # ~ sa.PrimaryKeyConstraint(vm_id, order),
        # ~ )  
            
    def update(vm_name, boots):
        db.boot.remove(db.query(Boot).filter(Boot.vm_id == Vm.by_name(vm_name).id).delete())
        db.vm.boot.append([Boot(vm_id=Vm.by_name(vm_name).id, name=boot) for boot in boots]) 
        return True

    def list(vm_name):
        return db.query(Boot).filter(Boot.vm_id==Vm.by_name(vm_name).id).all()

    def get_vm_boots(vm_id):
        vm_boots = db.query(Vm_Boot).filter(Vm.Boot.vm_id == vm_id).all()
        boot_list = []
        for vm_boot in vm_boot:
            boot = db.query(BootXML).filter(BootXML.id == vm_boot.boot_id).first()
            boots_list.append({**boot._as_dict(), **vm_boot._as_dict()})
        return boots_list 
