from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///your_database.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
#metadata = MetaData()

def init_db():
    Base.metadata.create_all(bind=engine)



#postimport 
from .command import Command
from .user import User