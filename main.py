from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import crud, schemas, models
from utils import within_distance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db, address)

@app.get("/addresses/", response_model=list[schemas.Address])
def get_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)

@app.get("/addresses/nearby/")
def get_addresses_within_distance(lat: float, lon: float, radius_km: float, db: Session = Depends(get_db)):
    all_addresses = crud.get_addresses(db)
    nearby = [
        addr for addr in all_addresses
        if within_distance(lat, lon, addr.latitude, addr.longitude, radius_km)
    ]
    return nearby
