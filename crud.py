from sqlalchemy.orm import Session
from models import Address
from schemas import AddressCreate

def create_address(db: Session, address: AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session):
    return db.query(Address).all()

def get_address_by_id(db: Session, id: int):
    return db.query(Address).filter(Address.id == id).first()

def delete_address(db: Session, id: int):
    address = get_address_by_id(db, id)
    if address:
        db.delete(address)
        db.commit()
    return address
