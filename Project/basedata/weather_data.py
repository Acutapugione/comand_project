from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import create_engine, DateTime
engine = create_engine("sqlite:///mydb", echo=True)
from datetime import datetime

class Base(DeclarativeBase):
    ...
    
    
class Weather(Base):
    __tablename__ = "weather"
    datetime: Mapped["datetime"] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column(primary_key=True)
    longitude: Mapped[float] = mapped_column(primary_key=True)
    
Base.metadata.drop_all(engine)
    
Base.metadata.create_all(engine)
Session = sessionmaker(engine)

with Session() as session:
    w1 = Weather(datetime=datetime(2023, 12, 8, 19), latitude=11.5, longitude=10.11)
    w2 = Weather(datetime=datetime(2023, 12, 8, 20), latitude=11.5, longitude=10.11)
    session.add(w1)
    session.add(w2)
    session.commit()