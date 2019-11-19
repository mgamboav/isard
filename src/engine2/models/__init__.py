from common.connection_manager import engine
from sqlalchemy.orm import scoped_session, sessionmaker
db = scoped_session(sessionmaker(bind=engine))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from models.domain import *
from models.template import *
from models.hypervisor import *
