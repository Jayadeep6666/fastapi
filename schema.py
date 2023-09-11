from pydantic import BaseModel

class AddressBase(BaseModel):
    id: int
    location_name: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class AddressCreate(AddressBase):
    pass


class Addressid(AddressBase):
    id: int


    class Config:
        orm_mode = True

class AddressUpdate(AddressBase):
    latitude: float
    longitude: float


    class Config:
        orm_mode = True