# ~ from sqlalchemy import Table, Column, sa.String, sa.Integer
import sqlalchemy as sa
# ~ from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect as _inspect
from sqlalchemy.ext.declarative import declarative_base

import json
Base = declarative_base()

class BaseMixin(Base):
    __abstract__ = True
    # ~ id = db.Column(db.Integer, primary_key=True)

    def by_id(self, pk):
        return db.query(self.__class__).get(pk)

    def to_dict(self):
        """Returns model as dict of properties.
        Note:
            Removes SQLAlchemy fields included in self.__dict__
        """
        column_names = _inspect(self.__class__).columns.keys()
        return {k: self.__dict__[k] for k in column_names}    
