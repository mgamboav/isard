# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.orderinglist import ordering_list

# ~ from models.Base_mixin import BaseMixin as Base
from models.base_mixin import BaseMixin

from models.parser.xml_parser import XmlParser

# ~ from common.connection_manager import db_session
from common.connection_manager import engine
from sqlalchemy.orm import scoped_session, sessionmaker
db = scoped_session(sessionmaker(bind=engine))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)
    return default_function
    
class Domain_Vcpu(Base):
    __tablename__ = 'domain_vcpu'

    __table_args__ = (
            sa.UniqueConstraint("domain_id", "vcpu_id"),
        )
        
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    vcpu_id = sa.Column(sa.Integer, sa.ForeignKey('vcpu_xml.id'), primary_key=True)
    vcpus = sa.Column(sa.Integer, nullable=False)
    
    vcpu = relationship("VcpuXML", back_populates="domain")
    domain = relationship("Domain", back_populates="vcpu")
    
class Domain_Memory(Base):
    __tablename__ = 'domain_memory'

    __table_args__ = (
            sa.UniqueConstraint("domain_id", "memory_id"),
        )
        
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    memory_id = sa.Column(sa.Integer, sa.ForeignKey('memory_xml.id'), primary_key=True)
    unit = sa.Column(sa.String, default='MiB')
    mem = sa.Column(sa.Integer, nullable=False)
    maxmemory = sa.Column(sa.Integer, default=same_as('mem'))
    currentmemory = sa.Column(sa.Integer, default=same_as('mem'))
    
    memory = relationship("MemoryXML", back_populates="domain")
    domain = relationship("Domain", back_populates="memory")
            
class Domain_Media(Base):
    __tablename__ = 'domain_media'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    media_id = sa.Column(sa.Integer, sa.ForeignKey('media_xml.id'), primary_key=True)
    rpath = sa.Column(sa.String, nullable=False)
    bus = sa.Column(sa.String, nullable=False)
    dev = sa.Column(sa.String, nullable=False)
    # size = sa.Column(sa.Integer)
    format = sa.Column(sa.String, nullable=False)
    order = sa.Column(sa.Integer, nullable=False)
    
    medias = relationship("MediaXML", back_populates="domains")
    domain = relationship("Domain", back_populates="medias")

class Domain_Interface(Base):
    __tablename__ = 'domain_interface'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    interface_id = sa.Column(sa.Integer, sa.ForeignKey('interface_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer, nullable=False)
    source = sa.Column(sa.String, nullable=False)
    model = sa.Column(sa.String, nullable=False)
    mac = sa.Column(sa.String, nullable=False)
    
    interfaces = relationship("InterfaceXML", back_populates="domains")
    domains = relationship("Domain", back_populates="interfaces")

class Domain_Graphic(Base):
    __tablename__ = 'domain_graphic'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    graphic_id = sa.Column(sa.Integer, sa.ForeignKey('graphic_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer, nullable=False)
    
    graphic = relationship("GraphicXML", back_populates="domain")
    domain = relationship("Domain", back_populates="graphic")
        
class Domain_Video(Base):
    __tablename__ = 'domain_video'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    video_id = sa.Column(sa.Integer, sa.ForeignKey('video_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer, nullable=False)
    
    videos = relationship("VideoXML", back_populates="domains")
    domain = relationship("Domain", back_populates="videos")
      
class Domain(BaseMixin, Base):
    __tablename__ = 'domain'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    
    domain_xml_id = sa.Column(sa.Integer, sa.ForeignKey('domain_xml.id'), nullable=False)
    domain_xml = relationship("DomainXML")  
    boot = relationship("Boot", order_by="Boot.order",
                            collection_class=ordering_list('order'),
                            cascade="all, delete-orphan")
    # ~ bullets = relationship("Bullet", order_by="Bullet.position",
                            # ~ collection_class=ordering_list('position')
                                
    disk = relationship('Disk')
    medias = relationship("Domain_Media", 
                                        back_populates="domain")
    graphic = relationship("Domain_Graphic", 
                                        back_populates="domain")
    interfaces = relationship("Domain_Interface", 
                                        back_populates="domains")                                                                                                                                                                                                                                                
    videos = relationship("Domain_Video", 
                                        back_populates="domain") 
    memory = relationship("Domain_Memory", 
                                        back_populates="domain") 
    vcpu = relationship("Domain_Vcpu", 
                                        back_populates="domain")                                         
                                        
    # ~ memory = relationship('MemoryXML')
    # ~ vcpu = relationship('VcpuXML')
    # ~ vcpu = sa.Column(sa.Integer)
    # ~ memory = sa.Column(sa.Integer)

    def get_xml(domain_name):
        try:
            domain = Domain.by_name(domain_name)
            domain_tree = XmlParser(db.query(DomainXML).filter(DomainXML.id == domain.domain_xml_id).first().xml)
            domain_tree.domain_name_update(domain.name)
            domain_tree.domain_vcpu_update(VcpuXML.get_domain_vcpu(domain.id))
            domain_tree.domain_memory_update(MemoryXML.get_domain_memory(domain.id))
            for disk in Disk.get_domain_disks(domain.id):
                domain_tree.domain_disk_add(disk)
            for interface in InterfaceXML.get_domain_interfaces(domain.id):
                domain_tree.domain_interface_add(interface)         
            for graphic in GraphicXML.get_domain_graphics(domain.id):
                domain_tree.domain_graphic_add(graphic)  
            for video in VideoXML.get_domain_video(domain.id):
                domain_tree.domain_graphic_add(video) 
            return domain_tree.to_xml()

        except Exception as e:
            raise
        
class Disk(BaseMixin, Base):
    __tablename__ = 'disk'
    
    __table_args__ = (
            sa.UniqueConstraint("domain_id", "order"),
        )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    order = sa.Column(sa.Integer)
    
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) 
    
    xml_id = sa.Column(sa.Integer, sa.ForeignKey('disk_xml.id'), nullable=False)  
    xml = relationship('DiskXML')
    
    ppath = sa.Column(sa.String)
    rpath = sa.Column(sa.String)
    
    bus = sa.Column(sa.String)
    dev = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    format = sa.Column(sa.String)

    def __init__(self, domain_id, name, xml, ppath="/", rpath=".",bus="virtio", dev="vda", size=5, format="qcow2", order=1):
        self.name = name
        self.xml = xml
        self.domain_id = domain_id
        self.ppath = ppath
        self.rpath = rpath
        self.bus = bus
        self.dev = dev
        self.size = size
        self.format = format  
        self.order = order  

    def get_domain_disks(domain_id):
        disks = db.query(Disk).filter(Disk.id == domain_id).all()
        disks_list = []
        for disk in disks:
            disks_list.append({'name':disk.name,
                            'xml': db.query(DiskXML).filter(DiskXML.id == disk.xml_id).first().xml,
                            'ppath': disk.ppath,
                            'rpath': disk.rpath,
                            'bus': disk.bus,
                            'dev': disk.dev,
                            'size': disk.size,
                            'format': disk.format,
                            'order': disk.order})
        return disks_list

class MemoryXML(BaseMixin, Base):
    __tablename__ = 'memory_xml'
    
    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("domain_id"),
        # ~ )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    xml = sa.Column(sa.String, unique=True)

    domain = relationship("Domain_Memory", 
                                        back_populates="memory")      
    # ~ domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) 

    def get_domain_memory(domain_id):
        memory = db.query(MemoryXML).filter(MemoryXML.id == domain_id).first()
        mdata = db.query(Domain_Memory).filter(Domain_Memory.memory_id == memory.id).first()
        return {'xml': memory.xml,
                'unit': mdata.unit,
                'maxmemory':mdata.maxmemory,
                'memory': mdata.mem,
                'currentmemory': mdata.currentmemory}
        return memory_list  
        
class VcpuXML(BaseMixin, Base):
    __tablename__ = 'vcpu_xml'
    
    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("domain_id"),
        # ~ )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    xml = sa.Column(sa.String, unique=True)

    domain = relationship("Domain_Vcpu", 
                                        back_populates="vcpu")  
    # ~ domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) 

    def get_domain_vcpu(domain_id):
        vcpu = db.query(VcpuXML).filter(VcpuXML.id == domain_id).first()
        vdata = db.query(Domain_Vcpu).filter(Domain_Vcpu.vcpu_id == vcpu.id).first()
        return {'xml': vcpu.xml,
                'vcpu':vdata.vcpus}
                        
class DiskXML(BaseMixin, Base):
    __tablename__ = "disk_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

    # ~ def get_xml(disk_xml_name):
        # ~ return db.query(DiskXML).filter(DiskXML.id == Disk.by_name(disk_name).xml_id).first().xml
                
class DomainXML(BaseMixin, Base):
    __tablename__ = "domain_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

    # ~ def get_xml(domain_xml_name):
        # ~ return db.query(DomainXML).filter(DiskXML.id == Disk.by_name(disk_name).xml_id).first().xml
                
class MediaXML(BaseMixin, Base):
    __tablename__ = "media_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domains = relationship("Domain_Media", 
                                        back_populates="medias")      
    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class GraphicXML(BaseMixin, Base):
    __tablename__ = "graphic_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domain = relationship("Domain_Graphic", 
                                        back_populates="graphic")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

    def get_domain_graphics(domain_id):
        graphics = db.query(GraphicXML).filter(GraphicXML.id == domain_id).all()
        graphics_list = []
        for graphic in graphics:
            gdata = db.query(Domain_Graphic).filter(Domain_Graphic.graphic_id == graphic.id).first()
            graphics_list.append({'name':graphic.name,
                            'xml': graphic.xml,
                            'order': gdata.order})
        return graphics_list   
        
class VideoXML(BaseMixin, Base):
    __tablename__ = "video_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domains = relationship("Domain_Video", 
                                        back_populates="videos")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

    def get_domain_video(domain_id):
        videos = db.query(VideoXML).filter(VideoXML.id == domain_id).all()
        videos_list = []
        for video in videos:
            vdata = db.query(Domain_Video).filter(Domain_Video.video_id == video.id).first()
            videos_list.append({'name':video.name,
                            'xml': video.xml,
                            'order': vdata.order})
        return videos_list   
        
class InterfaceXML(BaseMixin, Base):
    __tablename__ = "interface_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domains = relationship("Domain_Interface", 
                                        back_populates="interfaces")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml   

    def get_domain_interfaces(domain_id):
        interfaces = db.query(InterfaceXML).filter(InterfaceXML.id == domain_id).all()
        interfaces_list = []
        for interface in interfaces:
            ifdata = db.query(Domain_Interface).filter(Domain_Interface.interface_id == interface.id).first()
            interfaces_list.append({'name':interface.name,
                            'xml': interface.xml,
                            'source': ifdata.source,
                            'mac': ifdata.mac,
                            'model': ifdata.model,
                            'order': ifdata.order})
        return interfaces_list   

class Boot(BaseMixin, Base):
    __tablename__ = "boot"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), nullable=False)
    order = sa.Column(sa.Integer, nullable=False)

    __table_args__ = (
            sa.UniqueConstraint(domain_id, name),
        )   
    # ~ __table_args__ = (
            # ~ sa.PrimaryKeyConstraint(domain_id, order),
        # ~ )  
            
    def update(domain_name, names):
        db.boot.remove(db.query(Boot).filter(Boot.domain_id == Domain.by_name(domain_name).id).delete())
        db.domain.boot.append([Boot(domain_id=Domain.by_name(domain_name).id, name=name) for name in names]) 
        return True

    def list(domain_name):
        return db.query(Boot).filter(Boot.domain_id==Domain.by_name(domain_name).id).all()
