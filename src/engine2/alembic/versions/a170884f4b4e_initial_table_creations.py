"""Initial table creations

Revision ID: a170884f4b4e
Revises: 
Create Date: 2019-11-03 23:19:39.259589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from desktop import *

Session = sessionmaker()
Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'a170884f4b4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()

    Base.metadata.create_all(bind=bind)

    session = Session(bind=bind)
    # ~ session._model_changes = False  # if you are using Flask-SQLAlchemy, this works around a bug

    # ~ f1 = Foo(name='f1')
    # ~ f2 = Foo(name='f2')
    # ~ b1 = Bar(name='b1')
    # ~ b2 = Bar(name='b2')

    # ~ f1.bars = [b1, b2]
    # ~ b2.foos.append(f2)

    # ~ session.add_all([f1, f2, b1, b2])
    session.commit()


def downgrade():
    pass
