from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# set up database
SQLALCHEMY_DATABASE_URL='sqlite:///sql_app.db'
engine=create_engine(
    SQLALCHEMY_DATABASE_URL,

)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()