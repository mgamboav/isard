import sys

sys.path.append("../../")

from models.domain import *
from common.connection_manager import db_session

def select_domain(id):
    with db_session() as db:
        domains = db.query(Domain).all()
        print(GraphicXML.get_xml(domains[0].id))
    return domains
    return [d.to_dict() for d in domains]

domains = select_domain('_admin_tetros')
with db_session() as db:
    print(Domain.get_xml('_admin_tetros'))
# ~ with db_session() as db:
    # ~ print(domains[0].graphic)
