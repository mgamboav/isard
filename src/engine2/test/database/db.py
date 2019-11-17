import sys

sys.path.append("../../")

from common.connection_manager import engine
from sqlalchemy.orm import scoped_session, sessionmaker
db = scoped_session(sessionmaker(bind=engine))

from models.domain import *

def select_domain(domain_name):
    print(Domain.get_xml(domain_name))

domains = select_domain('_t_e_s_t_')
# ~ print(Domain.get_xml('_admin_tetros'))
