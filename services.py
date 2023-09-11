from sqlalchemy.orm import Session
import schema
import models

def add_location_to_db(db: Session, location: schema.Addressid):
    """location
    this method will add a new record to database. and perform the commit and refresh operation to db
    :param db: database session object
    :param location: Object of class schema.location
    :return: a dictionary object of the record which has inserted
    """
    mv_details = models.Address(
        id=location.id,
        location_name=location.location_name,
        latitude=location.latitude,
        longitude=location.longitude,
        
    )
    db.add(mv_details)
    db.commit()
    db.refresh(mv_details)
    return models.Address(**location.dict())



def get_location_by_id(db: Session, address_id: int):
    """
    This method will return  details based on id
    :param db: database session object
    :param id: serial id of record or Primary Key
    :return: data row if exist else None
    """
    return db.query(models.Address).filter(models.Address.id == address_id).first()



def update_location_details(db: Session, address_id: int, details: schema.AddressUpdate):
    """
    this method will update the database
    :param db: database session object
    :param address_id: serial id of record or Primary Key
    :param details: Object of class schema.Addressupdate
    :return: updated movie record
    """
    db.query(models.Address).filter(models.Address.id == address_id).update(vars(details))
    db.commit()
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    """
    This method will return all details which are present in database
    :param db: database session object
    :param skip: the number of rows to skip before including them in the result
    :param limit: to specify the maximum number of results to be returned
    :return: all the row from database
    """
    return db.query(models.Address).offset(skip).limit(limit).all()


def delete_location_details_by_id(db: Session, address_id: int):
    """
    This will delete the record from database based on primary key
    :param db: database session object
    :param sl_id: serial id of record or Primary Key
    :return: None
    """
    try:
        db.query(models.Address).filter(models.Address.id == address_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)