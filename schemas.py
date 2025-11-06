from pydantic import BaseModel, Field

class AddressBase(BaseModel):
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    class Config:
        orm_mode = True
