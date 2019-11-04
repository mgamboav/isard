"""Initial table creations

Revision ID: a170884f4b4e
Revises: 
Create Date: 2019-11-03 23:19:39.259589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from db.desktop import Base, Boot, Interface, Graphic, Video, DiskBus, DiskFormat
# Iso, Floppy

Session = sessionmaker()
# ~ Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'a170884f4b4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ~ Base.metadata.create_all(engine)
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
    session.commit()


def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
