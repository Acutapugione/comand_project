from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    
    commands = relationship('Command', back_populates='user')

# #users_table = Table(
#     'users',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String(50), unique=True),
# )
