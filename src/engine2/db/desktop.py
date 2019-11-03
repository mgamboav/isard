from sqlalchemy import Column, String, Integer, Date

from db.hardware import Hardware


class Desktop(Hardware):
    __tablename__ = 'desktop'

    id = Column(String, primary_key=True)

    def __init__(self, id):
        self.id = id
