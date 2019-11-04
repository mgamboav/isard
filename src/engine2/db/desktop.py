# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa

desktop_boots = sa.Table('desktop_boots', Base.metadata,
    sa.Column('desktop_id', sa.Integer, sa.ForeignKey('desktop.id')),
    sa.Column('boot_id', sa.String, sa.ForeignKey('boot.id'))
    sa.Column('order', sa.Integer)
)

desktop_disks = sa.Table('desktop_disks', Base.metadata,
    sa.Column('desktop_id', sa.Integer, sa.ForeignKey('desktop.id')),
    sa.Column('disk_id', sa.Integer, sa.ForeignKey('disk.id'))
    sa.Column('order', sa.Integer)
)

desktop_isos = sa.Table('desktop_isos', Base.metadata,
    sa.Column('desktop_id', sa.Integer, sa.ForeignKey('desktop.id')),
    sa.Column('iso_id', sa.String, sa.ForeignKey('isos.id'))
    sa.Column('order', sa.Integer)
)

desktop_floppies = sa.Table('desktop_floppies', Base.metadata,
    sa.Column('desktop_id', sa.Integer, sa.ForeignKey('desktop.id')),
    sa.Column('floppy_id', sa.String, sa.ForeignKey('floppy.id'))
    sa.Column('order', sa.Integer)
)

desktop_interfaces = sa.Table('desktop_interfaces', Base.metadata,
    sa.Column('desktop_id', sa.Integer, sa.ForeignKey('desktop.id')),
    sa.Column('interface_id', sa.String, sa.ForeignKey('interface.id'))
    sa.Column('order', sa.Integer)
)

desktop_graphics = sa.Table('desktop_graphics', Base.metadata,
    sa.Column('desktop_id', sa.Integer, sa.ForeignKey('desktop.id')),
    sa.Column('graphic_id', sa.String, sa.ForeignKey('graphic.id'))
    sa.Column('order', sa.Integer)
)

class Desktop(Base):
    __tablename__ = 'desktop'

    id = sa.Column(sa.String, primary_key=True)

    boots = relationship(
        "Boots",
        secondary=desktop_boots,
        back_populates="desktop"
    )
    disks = relationship(
        "Disks",
        secondary=desktop_disks,
        back_populates="desktop"
    )
    isos = relationship(
        "Isos",
        secondary=desktop_isos,
        back_populates="desktop"
    )
    floppies = relationship(
        "Floppies",
        secondary=desktop_floppies,
        back_populates="desktop"
    )    
    graphics = relationship(
        "Graphics",
        secondary=desktop_graphics,
        back_populates="desktop"
    )   
    interfaces = relationship(
        "Interfaces",
        secondary=desktop_interfaces,
        back_populates="desktop"
    )    
    video = relationship("Video")
    vcpu = sa.Column(sa.Integer)
    memory = sa.Column(sa.Integer)

    def __init__(self, id):
        self.id = id	

	
class Disk(Base):
	__tablename__ = 'disk'
	
	id = sa.Column(sa.Integer, primary_key=True)
    desktop = relationship(
        "Desktops",
        secondary=desktop_disks,
        backref="disk"
    )
    
    rpath = sa.Column(sa.String)
    bus = relationship("DiskBus")
    dev = sa.Column(sa.String)
    size = sa.Column(sa.Integer)
    format = relationship("DiskFormat")
    
class DiskBus(Base):
	__tablename__ = "disk_bus"
	id = sa.Column(sa.String, primary_key=True)

class DiskFormat(Base):
	__tablename__ = "disk_format"
	id = sa.Column(sa.String, primary_key=True)

class Video(Base):
	__tablename__ = "video"
	id = sa.Column(sa.String, primary_key=True)

	ram = sa.Column(sa.Integer)
	vram = sa.Column(sa.Integer)
	model = sa.Column(sa.String)
	heads = sa.Column(sa.Integer)
	
class Boot(Base):
	__tablename__ = "boot"
	id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktops",
        secondary=desktop_boots,
        backref="boot"
    )

class Iso(Base):
	__tablename__ = "iso"
	id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktops",
        secondary=desktop_isos,
        backref="iso"
    )

class Floppy(Base):
	__tablename__ = "floppy"
	id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktops",
        secondary=desktop_floppies,
        backref="floppy"
    )
        
class Interface(Base):
	__tablename__ = "interface"
	id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktops",
        secondary=desktop_interfaces,
        backref="interface"
    )
	
	ifname = sa.Column(sa.String)
	model = sa.Column(sa.String)
	net = sa.Column(sa.String)
	type = sa.Column(sa.String)

class Graphic(Base):
	__tablename__ = "graphic"
	id = sa.Column(sa.String, primary_key=True)
    desktop = relationship(
        "Desktops",
        secondary=desktop_graphics,
        backref="graphic"
    )
    protocol = sa.Column(sa.String)
    
