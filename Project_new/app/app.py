from fastapi import FastAPI
from models import PrognosForecastDays, PrognosToday, PrognosTodayId
from database import SessionLocal, engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session() 
    try:
        yield db
    finally:
        db.close()

@app.post("/prognos_forecast_days/")
async def create_prognos_forecast_days(prognos_forecast_days: PrognosForecastDays, db: Session = get_db()):
    db.add(prognos_forecast_days)
    db.commit()
    db.refresh(prognos_forecast_days)
    return prognos_forecast_days

@app.post("/prognos_today/")
async def create_prognos_today(prognos_today: PrognosToday, db: Session = get_db()):
    db.add(prognos_today)
    db.commit()
    db.refresh(prognos_today)
    return prognos_today

@app.post("/prognos_today_id/")
async def create_prognos_today_id(prognos_today_id: PrognosTodayId, db: Session = get_db()):
    db.add(prognos_today_id)
    db.commit()
    db.refresh(prognos_today_id)
    return prognos_today_id
