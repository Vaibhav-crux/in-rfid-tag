from sqlalchemy.orm import sessionmaker
from app.config.db_config import engine
from app.model.allotedTags import AllotedTags
from app.model.vehicleRegistration import VehicleRegistration  # Import VehicleRegistration model

# Create a session for database interaction
Session = sessionmaker(bind=engine)

def fetch_alloted_tag_by_rfid(rfid_tag):
    """
    Fetches the vehicle details from VehicleRegistration or AllotedTags based on the given RFID tag.
    Prioritizes VehicleRegistration data if available.
    """
    session = Session()
    try:
        # First, try to fetch from VehicleRegistration
        registration_entry = session.query(VehicleRegistration).filter_by(rfidTag=rfid_tag).first()
        if registration_entry:
            # If found in VehicleRegistration, return details from here
            return {
                'rfidTag': registration_entry.rfidTag,
                'typeOfVehicle': registration_entry.typeOfVehicle.value,
                'vehicleNumber': registration_entry.vehicleNumber,
                'doNumber': registration_entry.doNumber,
                'transporter': registration_entry.transporter,
                'driverOwner': registration_entry.driverOwner,
                'weighbridgeNo': registration_entry.weighbridgeNo,
                'visitPurpose': registration_entry.visitPurpose,
                'placeToVisit': registration_entry.placeToVisit,
                'personToVisit': registration_entry.personToVisit,
                'validityTill': registration_entry.validityTill,
                'section': registration_entry.section,
                'shift': registration_entry.shift,
                'isRegistered': True
            }

        # If not found in VehicleRegistration, check AllotedTags
        tag_entry = session.query(AllotedTags).filter_by(rfidTag=rfid_tag).first()
        if tag_entry:
            return {
                'rfidTag': tag_entry.rfidTag,
                'typeOfVehicle': tag_entry.typeOfVehicle.value,
                'vehicleNumber': tag_entry.vehicleNumber,
                'regDate': tag_entry.regDate,
                'regTime': tag_entry.regTime,
                'blacklisted': tag_entry.blacklisted,
                'isRegistered': False
            }
        else:
            return None
    finally:
        session.close()
