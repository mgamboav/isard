# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect

from models.base_mixin import BaseMixin as Base

# ~ class Domain_Boot_Association(Base):
    # ~ __tablename__ = 'Domain_boot_association'

    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("domain_id", "order"),
            # ~ sa.Index("domain_id","boot_id"),
        # ~ )
        
    # ~ domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) #, primary_key=True)
    # ~ boot_id = sa.Column(sa.Integer, sa.ForeignKey('boot.id')) #, primary_key=True)
    # ~ order = sa.Column(sa.Integer, primary_key=True)
    
    # ~ boots = relationship("Boot", back_populates="domains")
    # ~ domain = relationship("domain", back_populates="boots")

# ~ class Domain_Disk(Base):
    # ~ __tablename__ = 'Domain_disk'

    # ~ domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    # ~ disk_id = sa.Column(sa.Integer, sa.ForeignKey('disk.id'), primary_key=True)
    # ~ order = sa.Column(sa.Integer)
    
    # ~ medias = relationship("Disk", back_populates="domains")
    # ~ domain = relationship("domain", back_populates="disks")
        
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
    domain = relationship("Domain", back_populates="interfaces")

class Domain_Graphic(Base):
    __tablename__ = 'domain_graphic'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    graphic_id = sa.Column(sa.Integer, sa.ForeignKey('graphic_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    graphic = relationship("GraphicXML", back_populates="domain")
    domain = relationship("Domain", back_populates="graphic")

    # ~ def __init__(self, domain=None):
        # ~ print("in __init__: ", domain)
        # ~ self.domain = domain
        # ~ # self.correspondent = correspondent

# ~ from sqlalchemy.ext.associationproxy import association_proxy
# ~ Graphic.members = association_proxy("graphic", "domain")
# ~ User.communities = association_proxy("memberships", "community")
        
class Domain_Video(Base):
    __tablename__ = 'domain_video'

    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), primary_key=True)
    graphic_id = sa.Column(sa.Integer, sa.ForeignKey('video_xml.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    videos = relationship("VideoXML", back_populates="domains")
    domain = relationship("Domain", back_populates="videos")
      
class Domain(Base):
    __tablename__ = 'domain'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

    # ~ domain_id boot order
    # ~ boots = relationship("Domain_Boot_Association", 
                        # ~ cascade="save-update, merge, delete, delete-orphan",
                        # ~ back_populates="domain")

    # ~ boot_id = sa.Column(sa.Integer, sa.ForeignKey('boot.id'))
    
    # ~ domain_xml_id = sa.Column(sa.Integer, sa.ForeignKey('domain_xml.id'))
    domain_xmls = relationship("DomainXML")
    
    boot = relationship("Boot")
    
    # One to One
    disk = relationship('Disk')
    
    # Many to Many
    medias = relationship("Domain_Media", 
                                        back_populates="domain")
                                        
    graphic = relationship("Domain_Graphic", 
                                        back_populates="domain")
                                        
    interfaces = relationship("Domain_Interface", 
                                        back_populates="domain")                                                                                                                                                                                                                                                

    videos = relationship("Domain_Video", 
                                        back_populates="domain") 
    # Many to One
    # ~ video_id = sa.Column(sa.Integer, sa.ForeignKey('video.id'))
    # ~ video = relationship("Video")
    
    vcpu = sa.Column(sa.Integer)
    memory = sa.Column(sa.Integer)

class Disk(Base):
    __tablename__ = 'disk'
    
    ### composite primary_key: domain_id+order
    __table_args__ = (
            sa.UniqueConstraint("domain_id", "order"),
        )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    order = sa.Column(sa.Integer)
    
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) 
    
    # ~ xml_id = sa.Column(sa.Integer, sa.ForeignKey('disk_xml.id'))  
    xml = relationship('DiskXML')
    
    rpath = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    dev = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    format = sa.Column(sa.String)

    def __init__(self, domain_id, name, rpath=".",bus="virtio", dev="vda", size=5, format="qcow2", order=1):
        self.name = name
        self.domain_id = domain_id
        self.rpath = rpath
        self.bus = bus
        self.dev = dev
        self.size = size
        self.format = format  
        self.order = order  

class DiskXML(Base):
    __tablename__ = "disk_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    disk_id = sa.Column(sa.Integer, sa.ForeignKey('disk.id'))  
    # ~ domains = relationship("Domain_Disk", 
                                        # ~ back_populates="disk_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class DomainXML(Base):
    __tablename__ = "domain_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) 
    # ~ domains = relationship("Domain_DomainXML_Association", 
                                        # ~ back_populates="domain_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class MediaXML(Base):
    __tablename__ = "media_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domains = relationship("Domain_Media", 
                                        back_populates="medias")      
    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class GraphicXML(Base):
    __tablename__ = "graphic_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domain = relationship("Domain_Graphic", 
                                        back_populates="graphic")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class VideoXML(Base):
    __tablename__ = "video_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domains = relationship("Domain_Video", 
                                        back_populates="videos")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

class InterfaceXML(Base):
    __tablename__ = "interface_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    domains = relationship("Domain_Interface", 
                                        back_populates="interfaces")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml   
        
        
        
        
                 
class Boot(Base):
    __tablename__ = "boot"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'))
    order = sa.Column(sa.Integer)
    
    def __init__(self, domain_id, name, order):
        self.domain_id = domain_id
        self.name = name


        

    
# ~ class Media(Base):
    # ~ __tablename__ = 'media'
    
    # ~ id = sa.Column(sa.Integer, primary_key=True)
    # ~ name = sa.Column(sa.String, unique=True)
    
    # ~ domains = relationship("Domain_Media_Association", 
                                        # ~ back_populates="medias")    
    
    # ~ rpath = sa.Column(sa.String)
    # ~ bus = sa.Column(sa.String)
    # ~ dev = sa.Column(sa.String)
    # ~ # size = sa.Column(sa.Integer)
    # ~ format = sa.Column(sa.String)

    # ~ def __init__(self, name, rpath=".",bus="virtio", dev="vda", size=5, format="qcow2"):
        # ~ self.name = name
        # ~ self.rpath = rpath
        # ~ self.bus = bus
        # ~ self.dev = dev
        # ~ self.size = size
        # ~ self.format = format
                
# ~ class Interface(Base):
    # ~ __tablename__ = "interface"
    # ~ id = sa.Column(sa.Integer, primary_key=True)
    # ~ name = sa.Column(sa.String, unique=True, nullable=False)
    # ~ xml = sa.Column(sa.String, unique=True, nullable=False)
    # ~ network = sa.Column(sa.String, nullable=False)
    
    # ~ domains = relationship("Domain_Interface_Association", 
                                        # ~ back_populates="interfaces")      
    
    # ~ def __init__(self, name, xml, network):
        # ~ self.name = name
        # ~ self.xml = xml
        # ~ self.network = network
        
# ~ class Graphic(Base):
    # ~ __tablename__ = "graphic"
    # ~ id = sa.Column(sa.Integer, primary_key=True)
    # ~ name = sa.Column(sa.String, unique=True, nullable=False)
    # ~ xml = sa.Column(sa.String, unique=True, nullable=False)
    
    # ~ domains = relationship("Domain_Graphic_Association", 
                                        # ~ back_populates="graphics")      

    # ~ def __init__(self, name, xml):
        # ~ self.name = name
        # ~ self.xml = xml

# ~ class Video(Base):
    # ~ __tablename__ = "video"
    # ~ id = sa.Column(sa.Integer, primary_key=True)
    # ~ name = sa.Column(sa.String, unique=True, nullable=False)
    # ~ xml = sa.Column(sa.String, unique=True, nullable=False)
    
    # ~ def __init__(self, name, xml):
        # ~ self.name = name
        # ~ self.xml = xml

    # ~ def __repr__(self):
        # ~ return json.dumps({'name':self.name,'model':self.xml})
