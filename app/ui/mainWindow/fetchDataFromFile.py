from datetime import datetime
from PyQt5.QtCore import QTimer
from sqlalchemy.orm.exc import NoResultFound
from app.config.refreshSession import create_session
from app.model.allotedTags import AllotedTags
from app.model.vehicleRegistration import VehicleRegistration
from app.model.vehicleInOut import VehicleInOut

def fetch_and_update_rfid(file_path, rfid_input_left, rfid_input_right, status_label, indicator_label, vehicle_info, window):
    """Fetches the RFID tag from the specified file and updates the provided text boxes."""
    rfid_tag = read_rfid_from_file(file_path)
    if rfid_tag:
        rfid_input_left.setText(rfid_tag)
        rfid_input_right.setText(rfid_tag)
        # After setting the RFID Tag, check its status in the AllotedTags table
        if not check_rfid_status_in_db(rfid_tag, status_label, indicator_label):
            # If RFID Tag is valid and not blacklisted, check in the VehicleRegistration table
            if check_vehicle_registration_in_db(rfid_tag, status_label, indicator_label, vehicle_info):
                # If vehicle is registered and validity is okay, check VehicleInOut table
                check_vehicle_in_out_status(rfid_tag, status_label, indicator_label, vehicle_info)

        # Schedule a reset of the UI after 5 seconds, regardless of the outcome
        QTimer.singleShot(5000, lambda: reset_ui(window, file_path, rfid_input_left, rfid_input_right, status_label, indicator_label, vehicle_info))

def read_rfid_from_file(file_path):
    """Reads the RFID tag from the specified file."""
    try:
        with open(file_path, "r") as file:
            return file.readline().strip()  # Read the first line and strip any extra whitespace
    except FileNotFoundError:
        print(f"RFID file not found: {file_path}")
        return ""

def check_rfid_status_in_db(rfid_tag, status_label, indicator_label):
    """Checks the RFID Tag in the AllotedTags table and updates the status label and indicator."""
    session = create_session()
    try:
        # Query the AllotedTags table for the given RFID Tag
        record = session.query(AllotedTags).filter_by(rfidTag=rfid_tag).one()
        
        if record.blacklisted:
            status_label.setText("Vehicle Blocked")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
            return True  # RFID found and blocked
        else:
            status_label.setText("Vehicle Found")
            indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")
            return False  # RFID found and not blocked
    except NoResultFound:
        status_label.setText("Vehicle not found")
        indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        return True  # RFID not found
    finally:
        session.close()

def check_vehicle_registration_in_db(rfid_tag, status_label, indicator_label, vehicle_info):
    """Checks the RFID Tag in the VehicleRegistration table and populates the vehicle information."""
    session = create_session()
    try:
        # Query the VehicleRegistration table for the given RFID Tag
        record = session.query(VehicleRegistration).filter_by(rfidTag=rfid_tag).one()

        # Check if the ValidityTill date has expired
        current_date = datetime.utcnow().date()
        validity_till_date = datetime.strptime(record.validityTill, "%d/%m/%Y").date()  # Adjusted date format

        if validity_till_date < current_date:
            status_label.setText("Vehicle Validity Expire")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
            return False  # RFID found but validity expired

        # Populate the vehicle information into the respective text boxes on the left and right forms
        vehicle_info['typeOfVehicleLeft'].setText(record.typeOfVehicle.name)
        vehicle_info['vehicleNumberLeft'].setText(record.vehicleNumber)
        vehicle_info['validityTillLeft'].setText(record.validityTill)

        vehicle_info['typeOfVehicleRight'].setText(record.typeOfVehicle.name)
        vehicle_info['vehicleNumberRight'].setText(record.vehicleNumber)
        vehicle_info['doNumber'].setText(record.doNumber)
        vehicle_info['transporter'].setText(record.transporter)
        vehicle_info['driverOwner'].setText(record.driverOwner)
        vehicle_info['weighbridgeNo'].setText(record.weighbridgeNo)
        vehicle_info['visitPurpose'].setText(record.visitPurpose)
        vehicle_info['placeToVisit'].setText(record.placeToVisit)
        vehicle_info['personToVisit'].setText(record.personToVisit)
        vehicle_info['validityTillRight'].setText(record.validityTill)
        vehicle_info['section'].setText(record.section)

        # Update the status and indicator
        status_label.setText("Vehicle Registered")
        indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")
        return True  # RFID found and validity is okay
    except NoResultFound:
        status_label.setText("Vehicle Not Registered")
        indicator_label.setStyleSheet("background-color: yellow; border-radius: 10px;")
        return False  # RFID not found in VehicleRegistration
    finally:
        session.close()

def check_vehicle_in_out_status(rfid_tag, status_label, indicator_label, vehicle_info):
    """Checks the RFID Tag in the VehicleInOut table and handles vehicle entry if necessary."""
    session = create_session()
    try:
        # Query the VehicleInOut table for the latest entry for the given RFID Tag
        record = session.query(VehicleInOut).filter_by(rfidTag=rfid_tag).order_by(VehicleInOut.createdAt.desc()).first()

        if record and not record.dateOut and not record.timeOut:
            status_label.setText("Vehicle Not Out")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        else:
            # If no record exists or the last record has dateOut and timeOut, insert a new entry
            new_entry = VehicleInOut(
                rfidTag=rfid_tag,
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

            status_label.setText("Allowed Vehicle to In")
            indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")

    except Exception as e:
        status_label.setText("Error Handling Vehicle In")
        indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        print(f"Error: {e}")
    finally:
        session.close()

def reset_ui(window, file_path, rfid_input_left, rfid_input_right, status_label, indicator_label, vehicle_info):
    """Resets the UI after the action is completed."""
    # Clear the text boxes
    rfid_input_left.clear()
    rfid_input_right.clear()
    for key in vehicle_info:
        vehicle_info[key].clear()

    # Reset the status label and indicator
    status_label.setText("Waiting")
    indicator_label.setStyleSheet("background-color: grey; border-radius: 10px;")

    # Clear the text file
    with open(file_path, "w") as file:
        file.write("")
