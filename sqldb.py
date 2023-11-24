from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

engine = create_engine('sqlite:///your_database.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

Base = declarative_base()

metadata = MetaData()
class User(Base):

    your_table = Table(
    'user',
    MetaData,
    Column('id',Integer, primary_key=True),
    Column('username',String(50), unique=True),
    relationship('commands','Command', back_populates='user'),
    )

class Command(Base):
     your_table = Table(
     Column('id',Integer, primary_key=True),  
     Column('text',String(225)),
     Column('timestamp', DateTime, default=datetime.utcnow),
     Column('user_id',Integer, ForeignKey('users.id') ),
     Column('user',relationship,back_populates='commands')
    )
