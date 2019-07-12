from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,String,Integer
Model=declarative_base()
class Players(Model):
    __tablename__="players"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    image_link=Column(String)
    height=Column(Integer)
    weight=Column(Integer)
    dob=Column(String)
    place=Column(String)
    position=Column(String)

    def __repr__(self):
        return "<Players %s>" % self.name
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}    