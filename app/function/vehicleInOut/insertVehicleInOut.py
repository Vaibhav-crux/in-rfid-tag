from app.config.db_config import SessionLocal
from app.model.vehicleInOut import VehicleInOut
from datetime import datetime

def insert_vehicle_in_out_from_alloted_tag(alloted_tag):
    session = SessionLocal()
    try:
        # Check if the RFID tag or vehicle number already exists in the table
        existing_entry = session.query(VehicleInOut).filter(
            (VehicleInOut.rfidTag == alloted_tag['rfidTag']) | 
            (VehicleInOut.vehicleNumber == alloted_tag['vehicleNumber'])
        ).order_by(VehicleInOut.createdAt.desc()).first()  # Fetch the latest entry
        
        # If an existing entry is found
        if existing_entry:
            # Check if the vehicle has been marked as 'out'
            if not existing_entry.dateOut or not existing_entry.timeOut:
                # Vehicle hasn't been marked as 'out'
                print("Vehicle didn't out. Cannot insert a new entry.")
                # Update the widget's status and indicator to show vehicle not out
                return "Vehicle Not Out"

        # If no existing entry is found or the vehicle is marked as 'out', insert new data
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
            user=alloted_tag.get('user', ''),  # Save user if found on textbox, else keep empty
            shift=alloted_tag.get('shift', ''),  # Save shift if found on textbox, else keep empty
            barrierStatus='CLOSED'  # Default status
        )

        session.add(vehicle_in_out)
        session.commit()
        print(f"VehicleInOut entry added for RFID: {alloted_tag['rfidTag']}")
        return "Success"  # Indicate success to the calling function

    except Exception as e:
        session.rollback()
        print(f"Failed to insert VehicleInOut entry: {e}")
        return "Error"  # Indicate an error occurred
    finally:
        session.close()
