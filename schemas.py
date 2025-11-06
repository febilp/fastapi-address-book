"""
schemas.py
------------
Defines Pydantic models for request validation and response serialization.
Ensures data integrity through type enforcement and coordinate validation.
"""

from pydantic import BaseModel, Field

class AddressBase(BaseModel):
    """Shared attributes for all address-related schemas."""
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AddressCreate(AddressBase):
    """Schema for creating new address records."""
    pass

class Address(AddressBase):
    """Response schema with database-generated ID."""
    id: int
    class Config:
        orm_mode = True
