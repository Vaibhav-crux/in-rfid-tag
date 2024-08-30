# app/function/database_functions.py

from sqlalchemy.orm.exc import NoResultFound
from app.config.refreshSession import create_session
from app.model.allotedTags import AllotedTags
from app.model.vehicleRegistration import VehicleRegistration
from app.model.vehicleInOut import VehicleInOut
from datetime import datetime

def check_rfid_status_in_db(rfid_tag):
    """Checks the RFID Tag in the AllotedTags table and returns its status."""
    session = create_session()
    try:
        # Query the AllotedTags table for the given RFID Tag
        record = session.query(AllotedTags).filter_by(rfidTag=rfid_tag).one()
        
        if record.blacklisted:
            return "blocked"  # RFID found and blocked
        else:
            return "found"  # RFID found and not blocked
    except NoResultFound:
        return "not_found"  # RFID not found
    finally:
        session.close()

def check_vehicle_registration_in_db(rfid_tag):
    """Checks the RFID Tag in the VehicleRegistration table and returns the vehicle record."""
    session = create_session()
    try:
        # Query the VehicleRegistration table for the given RFID Tag
        record = session.query(VehicleRegistration).filter_by(rfidTag=rfid_tag).one()
        return record  # Return the found record
    except NoResultFound:
        return None  # RFID not found in VehicleRegistration
    finally:
        session.close()

def check_vehicle_in_out_status(rfid_tag):
    """Checks the RFID Tag in the VehicleInOut table and returns the latest entry."""
    session = create_session()
    try:
        # Query the VehicleInOut table for the latest entry for the given RFID Tag
        record = session.query(VehicleInOut).filter_by(rfidTag=rfid_tag).order_by(VehicleInOut.createdAt.desc()).first()
        return record  # Return the found record or None if not found
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        session.close()

def insert_vehicle_in_out_entry(vehicle_info):
    """Inserts a new entry into the VehicleInOut table."""
    session = create_session()
    try:
        new_entry = VehicleInOut(
            rfidTag=vehicle_info['rfidInputRight'].text(),
            typeOfVehicle=vehicle_info['typeOfVehicleRight'].text(),
            vehicleNumber=vehicle_info['vehicleNumberRight'].text(),
            doNumber=vehicle_info['doNumber'].text(),
            transporter=vehicle_info['transporter'].text(),
            driverOwner=vehicle_info['driverOwner'].text(),
            weighbridgeNo=vehicle_info['weighbridgeNo'].text(),
            visitPurpose=vehicle_info['visitPurpose'].text(),
            placeToVisit=vehicle_info['placeToVisit'].text(),
            personToVisit=vehicle_info['personToVisit'].text(),
            validityTill=vehicle_info['validityTillRight'].text(),
            section=vehicle_info['section'].text(),
            dateIn=datetime.utcnow().strftime("%Y-%m-%d"),
            timeIn=datetime.utcnow().strftime("%H:%M:%S"),
            user="System",  # Replace with actual user if available
            shift="Default",  # Replace with actual shift if available
        )
        session.add(new_entry)
        session.commit()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()
