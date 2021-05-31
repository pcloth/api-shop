from . import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, comment='ID')
    name = Column(String(50), unique=True, comment='姓名')
    email = Column(String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % (self.name)