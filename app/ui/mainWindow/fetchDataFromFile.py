# app/ui/mainWindow/fetchDataFromFile.py

from datetime import datetime
from PyQt5.QtCore import QTimer
from app.function.database_functions import (
    check_rfid_status_in_db,
    check_vehicle_registration_in_db,
    check_vehicle_in_out_status,
    insert_vehicle_in_out_entry
)

def fetch_and_update_rfid(file_path, rfid_input_left, rfid_input_right, status_label, indicator_label, vehicle_info, window):
    """Fetches the RFID tag from the specified file and updates the provided text boxes."""
    rfid_tag = read_rfid_from_file(file_path)
    if rfid_tag:
        rfid_input_left.setText(rfid_tag)
        rfid_input_right.setText(rfid_tag)

        # Check the RFID status in the AllotedTags table
        rfid_status = check_rfid_status_in_db(rfid_tag)
        if rfid_status == "blocked":
            status_label.setText("Vehicle Blocked")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        elif rfid_status == "not_found":
            status_label.setText("Vehicle not found")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        else:
            # RFID found, check vehicle registration
            record = check_vehicle_registration_in_db(rfid_tag)
            if record:
                # Check if the ValidityTill date has expired
                current_date = datetime.utcnow().date()
                validity_till_date = datetime.strptime(record.validityTill, "%d/%m/%Y").date()

                if validity_till_date < current_date:
                    status_label.setText("Vehicle Validity Expire")
                    indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
                else:
                    # Populate the vehicle information
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

                    # Check the VehicleInOut status
                    vehicle_in_out_record = check_vehicle_in_out_status(rfid_tag)
                    if vehicle_in_out_record and not vehicle_in_out_record.dateOut and not vehicle_in_out_record.timeOut:
                        status_label.setText("Vehicle Not Out")
                        indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
                    else:
                        # Insert a new VehicleInOut entry
                        insert_vehicle_in_out_entry(vehicle_info)
                        status_label.setText("Allowed Vehicle to In")
                        indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")
            else:
                status_label.setText("Vehicle Not Registered")
                indicator_label.setStyleSheet("background-color: yellow; border-radius: 10px;")

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
