from sqlalchemy import Column, Integer, String, Table, ForeignKey,Staff
from sqlalchemy.orm import relationship,Mapped,Staff,mapped_column
from . import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    
    commands: Mapped["Staff"] =relationship('Command', back_populates='user')
