# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.declarative import declarative_base
# ~ from common.connection_manager import db_session

from common.connection_manager import engine
from sqlalchemy.orm import scoped_session, sessionmaker
db = scoped_session(sessionmaker(bind=engine))

import json
Base = declarative_base()

class BaseMixin(Base):
    __abstract__ = True
    # ~ id = db.Column(db.Integer, primary_key=True)

    # ~ @classmethod
    # ~ def get_by(cls, **kw):
        # ~ return Session.query(cls).filter_by(**kw).first()
    
    # ~ @classmethod
    def by_name(self,name):
        with db_session as db:
            return db.query(self.__class__).get(name)

    # ~ def id_by_name(domain_name):
        # ~ with db_session() as db:
            # ~ return db.query(Domain).filter(Domain.name == domain_name).one().id
            
    # ~ def to_dict(self):
        # ~ """Returns model as dict of properties.
        # ~ Note:
            # ~ Removes SQLAlchemy fields included in self.__dict__
        # ~ """
        # ~ column_names = _inspect(self.__class__).columns.keys()
        # ~ return {k: self.__dict__[k] for k in column_names}   
    
    # ~ def __repr__(self):
        # ~ return '<{} {}>'.format(self.__class__.__name__, self.name)


    # ~ @classmethod
    # ~ def complex_cls_method(cls, key, values):
        # ~ main = cls(keyword=key, value="")
        # ~ ids = [cls(keyword=key, value=item, parent=main) for item in values]
        # ~ return [main] + ids  
