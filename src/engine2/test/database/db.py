import sys

sys.path.append("../../")

from models.domain import *
import models 

def select_domain(domain_name):
    print(Domain.get_xml(domain_name))

domains = select_domain('_t_e_s_t_')
# ~ print(Domain.get_xml('_admin_tetros'))
