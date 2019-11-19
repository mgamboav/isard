from models import db, Base
from models.base_mixin import BaseMixin

from models.vm import Vm
      
class Template(Vm):
    __mapper_args__ = {
        'polymorphic_identity':'template'
    }
