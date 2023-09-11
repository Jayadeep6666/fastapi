import logging
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from pydantic import BaseModel

from database import engine, Base
from database import get_db
from schema import AddressBase,  AddressCreate, Addressid, AddressUpdate
from sqlalchemy.orm import Session
import models ,services


app = FastAPI()


# Configure logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
@app.post("/address",response_model = Addressid)
def create_address(address: Addressid,db: Session = Depends(get_db)):

    if address.id is None or address.id <=0 :
        raise HTTPException(status_code=400, detail = "Invalid address id")

    # Check if the specific condition is met using address.id
    address_id = services.get_location_by_id(db=db, address_id=address.id)
    if address_id:
        raise HTTPException(status_code=400, detail=f"address id {address.id} already exist in database: {address.id}")
    result = services.add_location_to_db(db=db, location=address)
    # Log success
    logger.info(f"Created address: {result}")
    return result




@app.put('/update_location_details', response_model=AddressUpdate)
def update_location_details(address_id: int, update_param: AddressUpdate, db: Session = Depends(get_db)):

        details = services.get_location_by_id(db=db, address_id=address_id)
        if not details:
            raise HTTPException(status_code=404, detail=f"No record found to update")

        result =  services.update_location_details(db=db, details=update_param, address_id=address_id)
        logger.info(f"Address id {address_id} has been successfully updated.")
        return result



@app.get('/retrieve_all_movies_details', response_model=List[AddressBase])
def retrieve_all_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        locations = services.get_locations(db=db, skip=skip, limit=limit)
        logger.info("Data retrived")
        return locations
    except Exception as e:
        logger.error(f"Failed to retrieve addresses: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve addresses: {e}")


@app.delete('/delete_movie_by_id')
def delete_location_by_id(address_id: int, db: Session = Depends(get_db)):
    details = services.get_location_by_id(db=db, address_id=address_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    services.delete_location_details_by_id(db=db, address_id=address_id)

    return {"delete status": "success"}
