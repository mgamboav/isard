# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect

from models.base_mixin import BaseMixin as Base

# ~ class Desktop_Boot_Association(Base):
    # ~ __tablename__ = 'desktop_boot_association'

    # ~ __table_args__ = (
            # ~ sa.UniqueConstraint("desktop_id", "order"),
            # ~ sa.Index("desktop_id","boot_id"),
        # ~ )
        
    # ~ desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id')) #, primary_key=True)
    # ~ boot_id = sa.Column(sa.Integer, sa.ForeignKey('boot.id')) #, primary_key=True)
    # ~ order = sa.Column(sa.Integer, primary_key=True)
    
    # ~ boots = relationship("Boot", back_populates="desktops")
    # ~ desktop = relationship("Desktop", back_populates="boots")

class Desktop_Disk(Base):
    __tablename__ = 'desktop_disk'

    desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id'), primary_key=True)
    disk_id = sa.Column(sa.Integer, sa.ForeignKey('disk.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    medias = relationship("Disk", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="disks")
        
class Desktop_Media(Base):
    __tablename__ = 'desktop_media'

    desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id'), primary_key=True)
    media_id = sa.Column(sa.Integer, sa.ForeignKey('media.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    medias = relationship("Media", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="medias")

class Desktop_Interface(Base):
    __tablename__ = 'desktop_interface'

    desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id'), primary_key=True)
    interface_id = sa.Column(sa.Integer, sa.ForeignKey('interface.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    model = sa.Column(sa.String)
    
    interfaces = relationship("Interface", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="interfaces")

class Desktop_Graphic(Base):
    __tablename__ = 'desktop_graphic'

    desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id'), primary_key=True)
    graphic_id = sa.Column(sa.Integer, sa.ForeignKey('graphic.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    graphics = relationship("Graphic", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="graphics")
  
class Desktop(Base):
    __tablename__ = 'desktop'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

    # ~ desktop_id boot order
    # ~ boots = relationship("Desktop_Boot_Association", 
                        # ~ cascade="save-update, merge, delete, delete-orphan",
                        # ~ back_populates="desktop")

    # ~ boot_id = sa.Column(sa.Integer, sa.ForeignKey('boot.id'))
    boot = relationship("Boot")
    
    # One to One
    disk = relationship('Disk')
    
    # Many to Many
    medias = relationship("Desktop_Media_Association", 
                                        back_populates="desktop")
                                        
    graphics = relationship("Desktop_Graphic_Association", 
                                        back_populates="desktop")
                                        
    interfaces = relationship("Desktop_Interface_Association", 
                                        back_populates="desktop")                                                                                                                                                                                                                                                
    # Many to One
    video_id = sa.Column(sa.Integer, sa.ForeignKey('video.id'))
    video = relationship("Video")
    
    vcpu = sa.Column(sa.Integer)
    memory = sa.Column(sa.Integer)

class DomainXML(Base):
    __tablename__ = "domain_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_DomainXML_Association", 
                                        back_populates="domain_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class DiskXML(Base):
    __tablename__ = "disk_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_DiskXML_Association", 
                                        back_populates="disk_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class MediaXML(Base):
    __tablename__ = "media_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_MediaXML_Association", 
                                        back_populates="media_xmls")      
    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class GraphicXML(Base):
    __tablename__ = "graphic_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_GraphicXML_Association", 
                                        back_populates="graphic_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml
        
class VideoXML(Base):
    __tablename__ = "video_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_VideoXML_Association", 
                                        back_populates="video_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

class InterfaceXML(Base):
    __tablename__ = "interface_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_InterfaceXML_Association", 
                                        back_populates="interface_xmls")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml   
        
        
        
        
                 
class Boot(Base):
    __tablename__ = "boot"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id'))
    order = sa.Column(sa.Integer)
    
    def __init__(self, desktop_id, name, order):
        self.desktop_id = desktop_id
        self.name = name


        
class Disk(Base):
    __tablename__ = 'disk'
    
    ### composite primary_key: desktop_id+order
    __table_args__ = (
            sa.UniqueConstraint("desktop_id", "order"),
        )
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    order = sa.Column(sa.Integer)
    
    desktop_id = sa.Column(sa.Integer, sa.ForeignKey('desktop.id'))  
    
    rpath = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    dev = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    format = sa.Column(sa.String)

    def __init__(self, desktop_id, name, rpath=".",bus="virtio", dev="vda", size=5, format="qcow2", order=1):
        self.name = name
        self.desktop_id = desktop_id
        self.rpath = rpath
        self.bus = bus
        self.dev = dev
        self.size = size
        self.format = format  
        self.order = order  
    
class Media(Base):
    __tablename__ = 'media'
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    
    desktops = relationship("Desktop_Media_Association", 
                                        back_populates="medias")    
    
    rpath = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    dev = sa.Column(sa.String)
    # ~ size = sa.Column(sa.Integer)
    format = sa.Column(sa.String)

    def __init__(self, name, rpath=".",bus="virtio", dev="vda", size=5, format="qcow2"):
        self.name = name
        self.rpath = rpath
        self.bus = bus
        self.dev = dev
        self.size = size
        self.format = format
                
class Interface(Base):
    __tablename__ = "interface"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    network = sa.Column(sa.String, nullable=False)
    
    desktops = relationship("Desktop_Interface_Association", 
                                        back_populates="interfaces")      
    
    def __init__(self, name, xml, network):
        self.name = name
        self.xml = xml
        self.network = network
        
class Graphic(Base):
    __tablename__ = "graphic"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    desktops = relationship("Desktop_Graphic_Association", 
                                        back_populates="graphics")      

    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

class Video(Base):
    __tablename__ = "video"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    def __init__(self, name, xml):
        self.name = name
        self.xml = xml

    def __repr__(self):
        return json.dumps({'name':self.name,'model':self.xml})
