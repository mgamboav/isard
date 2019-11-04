"""Initial table creations

Revision ID: a170884f4b4e
Revises: 
Create Date: 2019-11-03 23:19:39.259589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from db.desktop import Base

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
    session.commit()


def downgrade():
	Base.metadata.drop_all(engine)
