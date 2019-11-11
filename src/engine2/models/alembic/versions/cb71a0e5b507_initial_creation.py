"""Initial creation

Revision ID: cb71a0e5b507
Revises: 
Create Date: 2019-11-07 19:20:01.517946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models.domain import *
from models.snippets import XMLHelper

# ~ Base, domain, Boot, Interface, Graphic, Video, Disk, DiskBus, DiskFormat
# Iso, Floppy

Session = sessionmaker()


# revision identifiers, used by Alembic.
revision = 'cb71a0e5b507'
down_revision = None
branch_labels = None
depends_on = None

xml = XMLHelper()

graph=""


    
def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    
    session = Session(bind=bind)
    
    graphics = [GraphicXML('spice',graph)]
    session.bulk_save_objects(graphics)
    
    session.bulk_save_objects([DomainXML(name=x['name'], xml=x['xml']) for x in xml.get_virtinstalls()])

    g_spice = session.query(GraphicXML).filter(GraphicXML.name == 'spice').one()
    domain = Domain(name="_admin_tetros", vcpu = 1, memory = 768)
    dg = Domain_Graphic(domain=domain, graphic=g_spice, order=1)
    domain.graphic.append(dg)
    
    
        
    session.add(domain)    
    session.commit()

    # ~ print(Domain.get_xml("_amin_tetros"))

def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
    # ~ for tbl in reversed(Base.metadata.sorted_tables):
        # ~ engine.execute(tbl.delete())
