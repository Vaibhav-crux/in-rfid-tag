from app.config.db_config import SessionLocal
from app.model.vehicleInOut import VehicleInOut
from datetime import datetime

def insert_vehicle_in_out_from_alloted_tag(alloted_tag):
    session = SessionLocal()
    try:
        # Extract data from the dictionary (alloted_tag) and insert it into the VehicleInOut table
        vehicle_in_out = VehicleInOut(
            rfidTag=alloted_tag['rfidTag'],
            typeOfVehicle=alloted_tag['typeOfVehicle'],
            vehicleNumber=alloted_tag['vehicleNumber'],
            doNumber=alloted_tag.get('doNumber'),
            transporter=alloted_tag.get('transporter'),
            driverOwner=alloted_tag.get('driverOwner'),
            weighbridgeNo=alloted_tag.get('weighbridgeNo'),
            visitPurpose=alloted_tag.get('visitPurpose'),
            placeToVisit=alloted_tag.get('placeToVisit'),
            personToVisit=alloted_tag.get('personToVisit'),
            validityTill=alloted_tag.get('validityTill'),
            section=alloted_tag.get('section'),
            dateIn=datetime.now().strftime('%Y-%m-%d'),
            timeIn=datetime.now().strftime('%H:%M:%S'),
            user='default_user',  # Replace with actual user
            shift='default_shift',  # Replace with actual shift
            barrierStatus='CLOSED'  # Default status
        )
        
        session.add(vehicle_in_out)
        session.commit()
        print(f"VehicleInOut entry added for RFID: {alloted_tag['rfidTag']}")
    except Exception as e:
        session.rollback()
        print(f"Failed to insert VehicleInOut entry: {e}")
    finally:
        session.close()
