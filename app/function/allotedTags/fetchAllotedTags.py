from sqlalchemy.orm import sessionmaker
from app.config.db_config import engine
from app.model.allotedTags import AllotedTags

# Create a session for database interaction
Session = sessionmaker(bind=engine)

def fetch_alloted_tag_by_rfid(rfid_tag):
    """
    Fetches the AllotedTags entry that matches the given RFID tag.
    Returns a dictionary with the relevant fields if found.
    """
    session = Session()
    try:
        tag_entry = session.query(AllotedTags).filter_by(rfidTag=rfid_tag).first()
        if tag_entry:
            return {
                'rfidTag': tag_entry.rfidTag,
                'typeOfVehicle': tag_entry.typeOfVehicle.value,
                'vehicleNumber': tag_entry.vehicleNumber,
                'doNumber': tag_entry.doNumber,
                'transporter': tag_entry.transporter,
                'driverOwner': tag_entry.driverOwner,
                'weighbridgeNo': tag_entry.weighbridgeNo,
                'visitPurpose': tag_entry.visitPurpose,
                'placeToVisit': tag_entry.placeToVisit,
                'personToVisit': tag_entry.personToVisit,
                'validityTill': tag_entry.validityTill,
                'section': tag_entry.section
            }
        else:
            return None
    finally:
        session.close()
