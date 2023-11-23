from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///example.db', echo=True)

#TODO: use oop style to implement SQLAlchemy 
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('a', String),
    Column('b', Integer)
    
)

metadata.create_all(engine)
