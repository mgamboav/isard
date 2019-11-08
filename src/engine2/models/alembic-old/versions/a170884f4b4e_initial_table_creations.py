"""Initial table creations

Revision ID: a170884f4b4e
Revises: 
Create Date: 2019-11-03 23:19:39.259589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models.domain import *
# ~ Base, domain, Boot, Interface, Graphic, Video, Disk, DiskBus, DiskFormat
# Iso, Floppy

Session = sessionmaker()
# ~ Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'a170884f4b4e'
down_revision = None
branch_labels = None
depends_on = None

iface='''
<interface type="network">
   <source network="default"/>
</interface>
'''

graph='''

'''

vid='''

'''
def upgrade():

    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    
    session = Session(bind=bind)
    # ~ boots = [Boot('disk'),Boot('cdrom'),Boot('pxe'),Boot('floppy')]
    interfaces = [Interface('default',iface,'default')]
    graphics = [Graphic('spice',graph)]
    videos = [Video('qxl','qxl',1,65536,65536),Video('qxl32','qxl',1,32768,32768),Video('vga','vga',1,16384,16384)]
    # ~ disk_buses = [DiskBus('virtio'),DiskBus('ide'),DiskBus('sata')]
    # ~ disk_formats = [DiskFormat('qcow2'),DiskFormat('raw')]
    # ~ session.bulk_save_objects(boots)
    session.bulk_save_objects(interfaces)
    session.bulk_save_objects(graphics)        
    # ~ session.bulk_save_objects(videos)
    # ~ session.bulk_save_objects(disk_buses)
    # ~ session.bulk_save_objects(disk_formats)    

    ###### Create domain
    domain = Domain(name="_admin_tetros", vcpu = 1, memory = 768)
    session.add(domain)
    session.add(Boot(domain.id, 'pxe', 1))
    session.add(Boot(domain.id, 'disk', 2))
    
    ### Create new elements: disk
    # ~ disk1_bus= session.query(DiskBus).get('virtio')
    # ~ disk1_format = session.query(DiskFormat).get('qcow2')
    disk1 = Disk(domain.id,'_admin_tetros_disk', '/pepinillo', 'virtio', 'vda', 4, 'qcow2', 1)
    session.add(disk1)
    # ~ session.add(Disk('_admin_tetros_disk', '/pepinillo', disk1_bus, 'vda', 4, disk1_format))


    
    # ~ session.add(domain_Disk_Association(domain=domain, disk_id='_admin_tetros_disk', order = 1))
    # ~ session.add(domain_Boot_Association(domain=domain, boot_id='pxe', order = 1))
    session.add(domain_Graphic_Association(domain=domain, graphic_id='spice', order = 1))
    session.add(domain_Interface_Association(domain=domain, interface_id='default', order = 1))
    domain.video_id='qxl'
    
    session.add(domain)    
    session.commit()


def downgrade():
    # ~ op.execute("drop schema public CASCADE")
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)

    # ~ for tbl in reversed(Base.metadata.sorted_tables):
        # ~ engine.execute(tbl.delete())
