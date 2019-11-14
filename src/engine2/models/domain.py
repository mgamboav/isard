# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.orderinglist import ordering_list

# ~ from models.Base_mixin import BaseMixin as Base
from models.base_mixin import BaseMixin

# ~ from common.connection_manager import db_session
from common.connection_manager import engine
from sqlalchemy.orm import scoped_session, sessionmaker
db = scoped_session(sessionmaker(bind=engine))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
        
class Domain_Media(Base):
    __tablename__ = 'domain_media'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    media_id = sa.Column(sa.Integer, sa.ForeignKey('media_xml.id'), primary_key=True)
    rpath = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    dev = sa.Column(sa.String)
    # size = sa.Column(sa.Integer)
    format = sa.Column(sa.String)
    order = sa.Column(sa.Integer)
    
    medias = relationship("MediaXML", back_populates="domains")
    domain = relationship("Domain", back_populates="medias")

class Domain_Interface(Base):
    __tablename__ = 'domain_interface'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    interface_id = sa.Column(sa.Integer, sa.ForeignKey('interface_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    model = sa.Column(sa.String)
    mac = sa.Column(sa.String)
    
    interfaces = relationship("InterfaceXML", back_populates="domains")
    domains = relationship("Domain", back_populates="interfaces")

class Domain_Graphic(Base):
    __tablename__ = 'domain_graphic'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    graphic_id = sa.Column(sa.Integer, sa.ForeignKey('graphic_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    graphic = relationship("GraphicXML", back_populates="domain")
    domain = relationship("Domain", back_populates="graphic")
        
class Domain_Video(Base):
    __tablename__ = 'domain_video'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    video_id = sa.Column(sa.Integer, sa.ForeignKey('video_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
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
                                        
    vcpu = sa.Column(sa.Integer)
    memory = sa.Column(sa.Integer)

    def get_xml(domain_name):
        domain = Domain.by_name(domain_name)
        domain_xml = db.query(DomainXML).filter(DomainXML.id == domain.domain_xml_id).first().xml
        disks = db.query(Disk).filter(Disk.id == domain.id).all()
        disks_xml = [db.query(DiskXML).filter(DiskXML.id == d.xml_id).first().xml for d in disks]
        disks_xml_str = ""
        for dx in disks_xml:
            disks_xml_str = disks_xml_str+dx
        return domain_xml + disks_xml_str

        
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
    
    rpath = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    dev = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    format = sa.Column(sa.String)

    def __init__(self, domain_id, name, xml, rpath=".",bus="virtio", dev="vda", size=5, format="qcow2", order=1):
        self.name = name
        self.xml = xml
        self.domain_id = domain_id
        self.rpath = rpath
        self.bus = bus
        self.dev = dev
        self.size = size
        self.format = format  
        self.order = order  

    # ~ def get_xml(disk_name):
        # ~ return db.query(DiskXML).filter(DiskXML.id == Disk.by_name(disk_name).xml_id).first().xml
        
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
