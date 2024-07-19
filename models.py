from sqlalchemy import Column,String, ForeignKey,Boolean
from database import Base
# from sqlalchemy.orm import relationship


#create models in database
class User(Base):
    __tablename__='users'
    id=Column(String, primary_key=True,index=True)
    name=Column(String,index=True)
   
   
class Task(Base):
    __tablename__='tasks'
    id=Column(String,primary_key=True,index=True)
    title=Column(String,index=True)
    description=Column(String,index=True)
    user_id=Column(String,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    complete=Column(Boolean,default=False)
   






