# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect

from models.base_mixin import BaseMixin as Base

import json
# ~ Base = declarative_base()

# ~ https://stackoverflow.com/questions/56388707/sqlalchemy-many-to-many-relationship-updating-association-object-with-extra-colu
# ~ class Set_Product_Association(Base):
    # ~ __tablename__ = 'set_product_association'

    # ~ set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), primary_key=True)
    # ~ product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)

    # ~ quantity = db.Column(db.Integer)

    # ~ product = db.relationship("Product", back_populates="sets")
    # ~ set = db.relationship("Set", back_populates="products")

# ~ class Set(Base):
    # ~ __tablename__ = 'sets'

    # ~ id = db.Column(db.Integer, primary_key=True)
    # ~ products = db.relationship("Set_Product_Association", 
                                        # ~ back_populates="set")

# ~ class Product(Base):
    # ~ __tablename__= 'products'

    # ~ id = db.Column(db.Integer, primary_key=True)
    # ~ part_number = db.Column(db.String(100), unique=True, nullable=False)
    # ~ sets = db.relationship("Set_Product_Association", 
                                     # ~ back_populates="product")
                                     
                                     

class Desktop_Boot_Association(Base):
    __tablename__ = 'desktop_boot_association'

    desktop_id = sa.Column(sa.String, sa.ForeignKey('desktop.id'), primary_key=True)
    boot_id = sa.Column(sa.String, sa.ForeignKey('boot.id')) #, primary_key=True)
    order = sa.Column(sa.Integer, primary_key=True)
    
    boots = relationship("Boot", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="boots")
    
# ~ desktop_boots = sa.Table('desktop_boots', Base.metadata,
    # ~ sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    # ~ sa.Column('boot_id', sa.String, sa.ForeignKey('boot.id')),
    # ~ sa.Column('order', sa.Integer)
# ~ )

class Desktop_Disk_Association(Base):
    __tablename__ = 'desktop_disk_association'

    desktop_id = sa.Column(sa.String, sa.ForeignKey('desktop.id'), primary_key=True)
    disk_id = sa.Column(sa.String, sa.ForeignKey('disk.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    disks = relationship("Disk", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="disks")
    
# ~ desktop_disks = sa.Table('desktop_disks', Base.metadata,
    # ~ sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    # ~ sa.Column('disk_id', sa.Integer, sa.ForeignKey('disk.id')),
    # ~ sa.Column('order', sa.Integer)
# ~ )

class Desktop_Iso_Association(Base):
    __tablename__ = 'desktop_iso_association'

    desktop_id = sa.Column(sa.String, sa.ForeignKey('desktop.id'), primary_key=True)
    iso_id = sa.Column(sa.String, sa.ForeignKey('iso.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    isos = relationship("Iso", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="isos")
    
# ~ desktop_isos = sa.Table('desktop_isos', Base.metadata,
    # ~ sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    # ~ sa.Column('iso_id', sa.String, sa.ForeignKey('iso.id')),
    # ~ sa.Column('order', sa.Integer)
# ~ )

class Desktop_Floppy_Association(Base):
    __tablename__ = 'desktop_floppy_association'

    desktop_id = sa.Column(sa.String, sa.ForeignKey('desktop.id'), primary_key=True)
    floppy_id = sa.Column(sa.String, sa.ForeignKey('floppy.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    floppies = relationship("Floppy", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="floppies")
    
# ~ desktop_floppies = sa.Table('desktop_floppies', Base.metadata,
    # ~ sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    # ~ sa.Column('floppy_id', sa.String, sa.ForeignKey('floppy.id')),
    # ~ sa.Column('order', sa.Integer)
# ~ )

class Desktop_Interface_Association(Base):
    __tablename__ = 'desktop_interface_association'

    desktop_id = sa.Column(sa.String, sa.ForeignKey('desktop.id'), primary_key=True)
    interface_id = sa.Column(sa.String, sa.ForeignKey('interface.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    interfaces = relationship("Interface", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="interfaces")

# ~ desktop_interfaces = sa.Table('desktop_interfaces', Base.metadata,
    # ~ sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    # ~ sa.Column('interface_id', sa.String, sa.ForeignKey('interface.id')),
    # ~ sa.Column('order', sa.Integer)
# ~ )

class Desktop_Graphic_Association(Base):
    __tablename__ = 'desktop_graphic_association'

    desktop_id = sa.Column(sa.String, sa.ForeignKey('desktop.id'), primary_key=True)
    graphic_id = sa.Column(sa.String, sa.ForeignKey('graphic.id'), primary_key=True)
    order = sa.Column(sa.Integer)
    
    graphics = relationship("Graphic", back_populates="desktops")
    desktop = relationship("Desktop", back_populates="graphics")
    
# ~ desktop_graphics = sa.Table('desktop_graphics', Base.metadata,
    # ~ sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    # ~ sa.Column('graphic_id', sa.String, sa.ForeignKey('graphic.id')),
    # ~ sa.Column('order', sa.Integer)
# ~ )

class Desktop(Base):
    __tablename__ = 'desktop'

    id = sa.Column(sa.String, primary_key=True)

    boots = relationship("Desktop_Boot_Association", 
                                        back_populates="desktop")

    disks = relationship("Desktop_Disk_Association", 
                                        back_populates="desktop")
                                        
    isos = relationship("Desktop_Iso_Association", 
                                        back_populates="desktop")
                                        
    floppies = relationship("Desktop_Floppy_Association", 
                                        back_populates="desktop")
                                        
    graphics = relationship("Desktop_Graphic_Association", 
                                        back_populates="desktop")
                                        
    interfaces = relationship("Desktop_Interface_Association", 
                                        back_populates="desktop")
                                                                                                                                                                                                                                                
    # ~ disks = relationship(
        # ~ "Disk",
        # ~ secondary=desktop_disks,
        # ~ #back_populates="desktop"
    # ~ )
  
    video_id = sa.Column(sa.String, sa.ForeignKey('video.id'))
    video = relationship("Video")
    vcpu = sa.Column(sa.Integer)
    memory = sa.Column(sa.Integer)

    # ~ def __init__(self, id, boots=['disk'], disks=None, isos=None, floppies=None, graphics=['spice'], interfaces=['default'], video=['qxl'], vcpu=1, memory=1024 ):
        # ~ self.id = id    
        # ~ self.boots = self.session.query(Boot).get(boots[0])
        # ~ if self.disks is None:
            # ~ disk = Disk(id=id)
        # ~ else:
            # ~ pass
        # ~ self.graphics = Graphic(graphics[0])
        # ~ self.interfaces = Interface(interfaces[0])
        # ~ self.video = video
        # ~ self.vcpu = vcpu
        # ~ self.memory = memory
            

    
    
class Disk(Base):
    __tablename__ = 'disk'
    
    id = sa.Column(sa.String, primary_key=True)
    
    ## this maybe should be a one-to-one relation??????
    ################################
    desktops = relationship("Desktop_Disk_Association", 
                                        back_populates="disks")    
    # ~ desktop = relationship(
        # ~ "Desktop",
        # ~ secondary=desktop_disks,
        # ~ # backref="disk"
    # ~ )
    
    rpath = sa.Column(sa.String)
    bus_id = sa.Column(sa.String, sa.ForeignKey('disk_bus.id'))
    bus = relationship("DiskBus")
    dev = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    format_id = sa.Column(sa.String, sa.ForeignKey('disk_format.id'))
    format = relationship("DiskFormat")

    def __init__(self, id, rpath=".",bus="virtio", dev="vda", size=5, format="qcow2"):
        self.id = id
        self.rpath = rpath
        self.bus = bus
        self.dev = dev
        self.size = size
        self.format = format
            
class DiskBus(Base):
    __tablename__ = "disk_bus"
    id = sa.Column(sa.String, primary_key=True)

    def __init__(self, id):
        self.id = id

class DiskFormat(Base):
    __tablename__ = "disk_format"
    id = sa.Column(sa.String, primary_key=True)

    def __init__(self, id):
        self.id = id
        
class Video(Base):
    __tablename__ = "video"
    id = sa.Column(sa.String, primary_key=True)

    ram = sa.Column(sa.Integer)
    vram = sa.Column(sa.Integer)
    model = sa.Column(sa.String)
    heads = sa.Column(sa.Integer)

    def __init__(self, id, model, heads, ram, vram):
        self.id = id
        self.model = model
        self.heads = heads
        self.ram = ram
        self.vram = vram

    # ~ def to_dict(self):
        # ~ """Returns model as dict of properties.
        # ~ Note:
            # ~ Removes SQLAlchemy fields included in self.__dict__
        # ~ """
        # ~ column_names = _inspect(self.__class__).columns.keys()
        # ~ return {k: self.__dict__[k] for k in column_names}
        
    def __repr__(self):
        return json.dumps({'id':self.id,'model':self.model})
        
class Boot(Base):
    __tablename__ = "boot"
    id = sa.Column(sa.String, primary_key=True)
    desktops = relationship("Desktop_Boot_Association", 
                            back_populates="boots")      
    # ~ desktops = relationship(
        # ~ "Desktop_Boot",
        # ~ secondary=desktop_boot_association,
        # ~ backref="boot"
    # ~ )
    def __init__(self, id):
        self.id = id
        
class Iso(Base):
    __tablename__ = "iso"
    id = sa.Column(sa.String, primary_key=True)
    desktops = relationship("Desktop_Iso_Association", 
                                        back_populates="isos")      
    # ~ desktop = relationship(
        # ~ "Desktop",
        # ~ secondary=desktop_isos,
        # ~ backref="iso"
    # ~ )

class Floppy(Base):
    __tablename__ = "floppy"
    id = sa.Column(sa.String, primary_key=True)
    desktops = relationship("Desktop_Floppy_Association", 
                                        back_populates="floppies")      
    # ~ desktop = relationship(
        # ~ "Desktop",
        # ~ secondary=desktop_floppies,
        # ~ backref="floppy"
    # ~ )
        
class Interface(Base):
    __tablename__ = "interface"
    id = sa.Column(sa.String, primary_key=True)
    desktops = relationship("Desktop_Interface_Association", 
                                        back_populates="interfaces")      
    # ~ desktop = relationship(
        # ~ "Desktop",
        # ~ secondary=desktop_interfaces,
        # ~ backref="interface"
    # ~ )
    
    ifname = sa.Column(sa.String)
    model = sa.Column(sa.String)
    net = sa.Column(sa.String)
    type = sa.Column(sa.String)

    def __init__(self, id, ifname, model, net, type):
        self.id = id
        self.ifname = ifname
        self.model = model
        self.net = net
        self.type = type
        
class Graphic(Base):
    __tablename__ = "graphic"
    id = sa.Column(sa.String, primary_key=True)
    desktops = relationship("Desktop_Graphic_Association", 
                                        back_populates="graphics")      
    # ~ desktop = relationship(
        # ~ "Desktop",
        # ~ secondary=desktop_graphics,
        # ~ backref="graphic"
    # ~ )
    protocol = sa.Column(sa.String)
    
    def __init__(self, id, protocol):
        self.id = id
        self.protocol = protocol
