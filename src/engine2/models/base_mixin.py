# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
from sqlalchemy.inspection import inspect as _inspect

from common.connection_manager import engine
from sqlalchemy.orm import scoped_session, sessionmaker
db = scoped_session(sessionmaker(bind=engine))

import json

class BaseMixin(object):
    
    @classmethod
    def by_name(self,name):
        return db.query(self).filter(self.name == name).first()

    @classmethod
    def __repr__(self):
        return '<{}>'.format(self.name)
        
    # ~ @classmethod
    # ~ def get_by(cls, **kw):
        # ~ return Session.query(cls).filter_by(**kw).first()
        
    # ~ @classmethod        
    # ~ def to_dict(self):
        # ~ """Returns model as dict of properties.
        # ~ Note:
            # ~ Removes SQLAlchemy fields included in self.__dict__
        # ~ """
        # ~ column_names = _inspect(self.__class__).columns.keys()
        # ~ return {k: self.__dict__[k] for k in column_names}   
    
    def _as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in _inspect(self).mapper.column_attrs}

