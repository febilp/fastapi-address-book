"""
main.py
--------
Main entry point of the FastAPI Address Book application.
Defines API routes, sets up logging, and initializes the database.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import crud, schemas, models
from utils import within_distance
import logging


# ---------------------------
# Configure application-wide logging
# ---------------------------
logging.basicConfig(
level=logging.INFO,
format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
handlers=[
logging.FileHandler("app.log"),
logging.StreamHandler()
]
)


logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

# Dependency injection for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# API ROUTES
# ---------------------------

@app.post("/addresses/", response_model=schemas.Address, status_code=201)
def api_create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """Endpoint to create a new address record."""
    logger.info(f"Received request to create address: {address.name}")
    return crud.create_address(db, address)




@app.get("/addresses/", response_model=list[schemas.Address])
def api_get_addresses(limit: int = Query(100, ge=1, le=1000), offset: int = 0, db: Session = Depends(get_db)):
    """Retrieve all addresses with pagination support."""
    logger.info(f"Fetching addresses limit={limit}, offset={offset}")
    return crud.get_addresses(db, limit=limit, offset=offset)




@app.get("/addresses/{address_id}", response_model=schemas.Address)
def api_get_address(address_id: int, db: Session = Depends(get_db)):
    """Retrieve a single address by ID."""
    db_obj = crud.get_address_by_id(db, address_id)
    if not db_obj:
        logger.warning(f"Address ID {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return db_obj




@app.put("/addresses/{address_id}", response_model=schemas.Address)
def api_update_address(address_id: int, address_in: schemas.AddressCreate, db: Session = Depends(get_db)):
    """Update an existing address record by ID."""
    logger.info(f"Updating address ID {address_id}")
    return crud.update_address(db, address_id, address_in)




@app.delete("/addresses/{address_id}")
def api_delete_address(address_id: int, db: Session = Depends(get_db)):
    """Delete an address record by ID."""
    logger.info(f"Deleting address ID {address_id}")
    crud.delete_address(db, address_id)
    return {"status": "deleted"}




@app.get("/addresses/nearby/", response_model=list[schemas.Address])
def api_get_addresses_nearby(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    ):
    """Retrieve all addresses within a given radius (km) of the provided coordinates."""
    logger.info(f"Searching addresses within {radius_km} km of ({lat}, {lon})")
    all_addresses = crud.get_addresses(db)
    nearby = [addr for addr in all_addresses if within_distance(lat, lon, addr.latitude, addr.longitude, radius_km)]
    logger.info(f"Found {len(nearby)} nearby addresses")
    return nearby




@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    logger.debug("Health check ping")
    return {"status": "ok"}