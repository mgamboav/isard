# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect

from models.base_mixin import BaseMixin as Base

import json
# ~ Base = declarative_base()

desktop_boots = sa.Table('desktop_boots', Base.metadata,
    sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    sa.Column('boot_id', sa.String, sa.ForeignKey('boot.id')),
    sa.Column('order', sa.Integer)
)

desktop_disks = sa.Table('desktop_disks', Base.metadata,
    sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    sa.Column('disk_id', sa.Integer, sa.ForeignKey('disk.id')),
    sa.Column('order', sa.Integer)
)

desktop_isos = sa.Table('desktop_isos', Base.metadata,
    sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    sa.Column('iso_id', sa.String, sa.ForeignKey('iso.id')),
    sa.Column('order', sa.Integer)
)

desktop_floppies = sa.Table('desktop_floppies', Base.metadata,
    sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    sa.Column('floppy_id', sa.String, sa.ForeignKey('floppy.id')),
    sa.Column('order', sa.Integer)
)

desktop_interfaces = sa.Table('desktop_interfaces', Base.metadata,
    sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    sa.Column('interface_id', sa.String, sa.ForeignKey('interface.id')),
    sa.Column('order', sa.Integer)
)

desktop_graphics = sa.Table('desktop_graphics', Base.metadata,
    sa.Column('desktop_id', sa.String, sa.ForeignKey('desktop.id')),
    sa.Column('graphic_id', sa.String, sa.ForeignKey('graphic.id')),
    sa.Column('order', sa.Integer)
)

class Desktop(Base):
    __tablename__ = 'desktop'

    id = sa.Column(sa.String, primary_key=True)

    boots = relationship(
        "Boot",
        secondary=desktop_boots,
        # ~ back_populates="desktop"
    )
    disks = relationship(
        "Disk",
        secondary=desktop_disks,
        # ~ back_populates="desktop"
    )
    isos = relationship(
        "Iso",
        secondary=desktop_isos,
        # ~ back_populates="desktop"
    )
    floppies = relationship(
        "Floppy",
        secondary=desktop_floppies,
        # ~ back_populates="desktop"
    )    
    graphics = relationship(
        "Graphic",
        secondary=desktop_graphics,
        # ~ back_populates="desktop"
    )   
    interfaces = relationship(
        "Interface",
        secondary=desktop_interfaces,
        # ~ back_populates="desktop"
    )    
    video_id = sa.Column(sa.String, sa.ForeignKey('video.id'))
    video = relationship("Video")
    vcpu = sa.Column(sa.Integer)
    memory = sa.Column(sa.Integer)

    def __init__(self, id, boots=['disk'], disks=None, isos=None, floppies=None, graphics=['spice'], interfaces=['default'], video=['qxl'], vcpu=1, memory=1024 ):
        self.id = id    
        self.boots = self.session.query(Boot).get(boots[0])
        if self.disks is None:
            disk = Disk(id=id)
        else:
            pass
        self.graphics = Graphic(graphics[0])
        self.interfaces = Interface(interfaces[0])
        self.video = video
        self.vcpu = vcpu
        self.memory = memory
            

    
    
class Disk(Base):
    __tablename__ = 'disk'
    
    id = sa.Column(sa.Integer, primary_key=True)
    desktop = relationship(
        "Desktop",
        secondary=desktop_disks,
        # ~ backref="disk"
    )
    
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
    desktop = relationship(
        "Desktop",
        secondary=desktop_boots,
        backref="boot"
    )
    def __init__(self, id):
        self.id = id
        
class Iso(Base):
    __tablename__ = "iso"
    id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktop",
        secondary=desktop_isos,
        backref="iso"
    )

class Floppy(Base):
    __tablename__ = "floppy"
    id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktop",
        secondary=desktop_floppies,
        backref="floppy"
    )
        
class Interface(Base):
    __tablename__ = "interface"
    id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktop",
        secondary=desktop_interfaces,
        backref="interface"
    )
    
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
    desktop = relationship(
        "Desktop",
        secondary=desktop_graphics,
        backref="graphic"
    )
    protocol = sa.Column(sa.String)
    
    def __init__(self, id, protocol):
        self.id = id
        self.protocol = protocol
