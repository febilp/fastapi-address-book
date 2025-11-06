"""
crud.py
--------
Contains all Create, Read, Update, and Delete operations for the Address model.
Includes logging for each database action to ensure traceability.
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Address
from schemas import AddressCreate
import models, schemas, logging


logger = logging.getLogger(__name__)

def create_address(db: Session, address: AddressCreate):
    """Create a new address record in the database."""
    logger.info(f"Creating new address: {address.name}")
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session, limit: int = 100, offset: int = 0):
    """Fetch all address records with optional pagination."""
    logger.debug(f"Fetching addresses with limit={limit}, offset={offset}")
    return db.query(Address).all()

def get_address_by_id(db: Session, address_id: int):
    """Retrieve a single address by its ID."""
    logger.debug(f"Fetching address with ID {address_id}")
    return db.query(Address).filter(Address.id == address_id).first()

def update_address(db: Session, address_id: int, address_in: schemas.AddressCreate):
    """Update an existing address record."""
    db_obj = get_address_by_id(db, address_id)
    if not db_obj:
        logger.warning(f"Address ID {address_id} not found for update")
        raise HTTPException(status_code=404, detail="Address not found")


    for field, value in address_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)


    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    logger.info(f"Updated address ID {address_id}")
    return db_obj

def delete_address(db: Session, address_id: int):
    """Delete an address record by ID."""
    db_obj = get_address_by_id(db, address_id)
    if not db_obj:
        logger.warning(f"Attempted to delete non-existing address ID {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")


    db.delete(db_obj)
    db.commit()
    logger.info(f"Deleted address ID {address_id}")
    return db_obj
