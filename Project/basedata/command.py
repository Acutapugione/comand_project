from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from . import Base
from dataclasses import dataclass


@dataclass
class Command(Base):
    __tablename__ = 'commands'

    id:  Mapped[int] = mapped_column (primary_key=True)
    text: Mapped[str] = mapped_column (String(225)
    timestamp: Mapped[str] = mapped_column (DateTime, default=datetime.utcnow)
    user_id = Mapped[int] = mapped_column (ForeignKey('users.id')
    
    user = relationship('User', back_populates='commands')

# commands_table = Table(
#     'commands',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('text', String(225)),
#     Column('timestamp', DateTime, default=datetime.utcnow),
#     Column('user_id', Integer, ForeignKey('users.id')),
# )
