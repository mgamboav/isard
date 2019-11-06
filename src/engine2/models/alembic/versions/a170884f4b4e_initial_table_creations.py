"""Initial table creations

Revision ID: a170884f4b4e
Revises: 
Create Date: 2019-11-03 23:19:39.259589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models.desktop import *
# ~ Base, Desktop, Boot, Interface, Graphic, Video, Disk, DiskBus, DiskFormat
# Iso, Floppy

Session = sessionmaker()
# ~ Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'a170884f4b4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    
    session = Session(bind=bind)
    boots = [Boot('disk'),Boot('cdrom'),Boot('pxe'),Boot('floppy')]
    interfaces = [Interface('default','default','virtio','','network')]
    graphics = [Graphic('spice','spice'), Graphic('vnc','vnc')]
    videos = [Video('qxl','qxl',1,65536,65536),Video('qxl32','qxl',1,32768,32768),Video('vga','vga',1,16384,16384)]
    disk_buses = [DiskBus('virtio'),DiskBus('ide'),DiskBus('sata')]
    disk_formats = [DiskFormat('qcow2'),DiskFormat('raw')]
    session.bulk_save_objects(boots)
    session.bulk_save_objects(interfaces)
    session.bulk_save_objects(graphics)        
    session.bulk_save_objects(videos)
    session.bulk_save_objects(disk_buses)
    session.bulk_save_objects(disk_formats)    

# ~ s = Set.query.get(2)
# ~ p = Product.query.get(3)
# ~ a = Set_Product_Association(set=s, product=p, quantity=23)
# ~ db.session.add(a)
# ~ db.session.commit()

# ~ set = desktop
# ~ product = boot
     # ~ id, boots=['disk'], disks=None, isos=None, floppies=None, graphics=['spice'], interfaces=['default'], video=['qxl'], vcpu=1, memory=1024 ):


    ### Create new elements: disk
    disk1_bus= session.query(DiskBus).get('virtio')
    disk1_format = session.query(DiskFormat).get('qcow2')
    disk1 = Disk('_admin_tetros_disk', '/pepinillo', disk1_bus, 'vda', 4, disk1_format)
    session.add(disk1)
    
    ### Get new elements: boots, graphics, interfaces, videos
    boot1 = session.query(Boot).get('disk') 
    boot2 = session.query(Boot).get('pxe') 
    graphic1 = session.query(Graphic).get('spice')
    interface1 = session.query(Interface).get('default')
    video1 = session.query(Video).get('qxl')
    
    ### Create Desktop
    desktop = Desktop(id="_admin_tetros", vcpu = 1, memory = 1024)
    session.add(desktop)
    
    ### Associate elements with desktop
    dda1 = Desktop_Disk_Association(desktop=desktop, disk_id=disk1.id, order = 1)
    session.add(dda1)
    desktop.disk_id=disk1.id
    
    dba1 = Desktop_Boot_Association(desktop=desktop, boot_id=boot1.id, order = 1)
    session.add(dba1)
    dba2 = Desktop_Boot_Association(desktop=desktop, boot_id=boot2.id, order = 2)
    session.add(dba2)    
    dga1 = Desktop_Graphic_Association(desktop=desktop, graphic_id='spice', order = 1)
    session.add(dga1)
    dia1 = Desktop_Interface_Association(desktop=desktop, interface_id=interface1.id, order = 1)
    session.add(dia1)
    desktop.video_id=video1.id
    # ~ dva1 = Desktop_Video_Association(desktop=desktop, video_id=video1, order = 1)
    # ~ session.add(dva1)
    
    session.add(desktop)    
    session.commit()


def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)

    # ~ for tbl in reversed(Base.metadata.sorted_tables):
        # ~ engine.execute(tbl.delete())
