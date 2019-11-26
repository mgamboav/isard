import sys

sys.path.append("../../")

from models.domain import Domain
from models.template import Template
from models.vm import *
from models.hypervisor import *
from models import db

# ~ def select_domain(domain_name):
    # ~ print(Domain.get_xml(domain_name))

# ~ domains = select_domain('_t_e_s_t_')
# ~ print(Domain.get_xml('_admin_tetros'))

vm = db.query(Vm).get(1)
print(vm)
    # ~ VmMemory memory = 4;
    # ~ VmVcpu vcpu = 5;
    # ~ VmCpu cpu = 6;
    # ~ repeated Boot boots = 7;
    # ~ repeated VmDisk disks = 8;
    # ~ repeated VmMedia medias = 9;
    # ~ repeated VmInterface interfaces = 10;
    # ~ repeated VmGraphic graphics = 11;
    # ~ repeated VmVideo videos = 12;
    # ~ repeated VmSound sounds = 13;



