import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.orderinglist import ordering_list

from models import db, Base
from models.base_mixin import BaseMixin

from models.domain import CpuXML

import enum

def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)
    return default_function

class DefaultModes(enum.Enum):
    secure = 1
    insecure = 2
    
class ViewerCertificate(BaseMixin, Base):
    __tablename__ = 'viewer_certificate'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    default_mode = sa.Column(sa.Enum(DefaultModes))
    certificate = sa.Column(sa.String, unique=True) 
    server_cert = sa.Column(sa.String, unique=True)
    host_subject = sa.Column(sa.String, unique=True)
    domain = sa.Column(sa.String, unique=True)    

class HypervisorPool(BaseMixin, Base):
    __tablename__ = 'hypervisor_pool'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

    viewer_certificate_id = sa.Column(sa.Integer, sa.ForeignKey('viewer_certificate.id'), nullable=False)
    viewer_certificate = relationship("ViewerCertificate")  
    
    # ~ interfaces = sa.Column(sa.Integer, )
    cpu_id = sa.Column(sa.Integer, sa.ForeignKey('cpu_xml.id'), default=1)
    cpu = relationship("CpuXML")  
    
    acl = relationship("Acl")
    
    # ~ path_groups =
    # ~ path_templates =
    # ~ path_media =


        
class Hypervisor(BaseMixin, Base):
    __tablename__ = 'hypervisor'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, default=same_as('hostname'))
    hostname = sa.Column(sa.String, unique=True)
    port =sa.Column(sa.Integer, default=22)
    user = sa.Column(sa.String, default='root')
    passwd = sa.Column(sa.String)
    certificate = sa.Column(sa.String)
    capability_hyper = sa.Column(sa.Boolean, default=True)
    capability_diskop = sa.Column(sa.Boolean, default=True)
    viewer_hostname = sa.Column(sa.String, default=same_as('hostname'))
    viewer_nat_hostname = sa.Column(sa.String, default=same_as('hostname'))
    viewer_nat_offset = sa.Column(sa.Integer, default=0)
    
    enabled = sa.Column(sa.Boolean, default=False)
    state = sa.Column(sa.String, default='STATE_DISCONNECTED')
    
    hypervisor_pool_id = sa.Column(sa.Integer, sa.ForeignKey('hypervisor_pool.id'))
    hypervisor_pool = relationship("HypervisorPool")   
    
    acl = relationship("Acl", uselist=False, back_populates="hypervisor")
    
    
class Acl(BaseMixin, Base):
    __tablename__ = 'acl'

    id = sa.Column(sa.Integer, primary_key=True)
    hypervisor_pool_id = sa.Column(sa.Integer, sa.ForeignKey('hypervisor_pool.id'), nullable=False)
    order = sa.Column(sa.Integer, nullable=False)    
    src = sa.Column(sa.String, unique=True)
    dst = sa.Column(sa.String, unique=True)
    weight = sa.Column(sa.Integer)
    actions = relationship("Actions")
    hypervisor_id = sa.Column(sa.Integer, sa.ForeignKey('hypervisor.id'))
    hypervisor = relationship("Hypervisor", back_populates="acl")

class Actions(BaseMixin, Base): 
    __tablename__ = 'actions'

    id = sa.Column(sa.Integer, primary_key=True)
    acl_id =  sa.Column(sa.Integer, sa.ForeignKey('acl.id'))
    acl = relationship("Acl", back_populates="actions")
