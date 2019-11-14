# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.orderinglist import ordering_list

from models.base_mixin import BaseMixin as Base

from common.connection_manager import db_session
        
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
      
class Domain(Base):
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

    def get_xml(name):
        # ~ print(self)
        with db_session() as db:
            domains = db.query(Domain).all()
            return(domains[0].graphic[0])
            # ~ return db.query(Domain).get(name)
            # ~ return db.query(self.__class__).get(name)
        # ~ self.tree.xpath(xpath).getparent().remove(self.tree.xpath(xpath))
    def id_by_name(domain_name):
        with db_session() as db:
            return db.query(Domain).filter(Domain.name == domain_name).first()
        
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

class DiskXML(Base):
    __tablename__ = "disk_xml"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    xml = sa.Column(sa.String, unique=True, nullable=False)
    
    # ~ disk_id = sa.Column(sa.Integer, sa.ForeignKey('disk.id'))  
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
    
    # ~ domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id')) 
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
    name = sa.Column(sa.String, nullable=False)
    domain_id = sa.Column(sa.Integer, sa.ForeignKey('domain.id'), nullable=False)
    order = sa.Column(sa.Integer, nullable=False)

    __table_args__ = (
            sa.UniqueConstraint(domain_id, name),
        )   
    # ~ __table_args__ = (
            # ~ sa.PrimaryKeyConstraint(domain_id, order),
        # ~ )  
            
    # ~ def __init__(self, domain_id, name, order):
        # ~ self.domain_id = domain_id
        # ~ self.name = name
        # ~ self.order = order
    
    def update(domain_name, names):
        # ~ #print(self)
        with db_session() as db:
            db.boot.remove(db.query(Boot).filter(Boot.domain_id == domain_id).delete())
            db.domain.boot.append([Boot(domain_id=domain.id, name=name) for name in names]) 
            return True
            # ~ boot = Boot(domain_id=domain.id, name=name)
            # ~ try: 
                # ~ db.boot.insert(1,boot)
                # ~ db.domain.boot.insert(1,db)
            # ~ except Exception as IntegrityError:
                # ~ db.bootremove(db.query(Boot).filter(Boot.name == name).one()) 
                # ~ db.domain.boot.insert(1,boot)
    def list(domain_name):
        with db_session() as db:
            return db.query(Boot).filter(Boot.domain_id==str(Domain.id_by_name(domain_name).id)).all()
            # ~ eturn db.query(Boot).filter(Boot.domain_id==Domain.id_by_name(domain_name).id).all()
    # ~ def remove(self,domain_id, name):
