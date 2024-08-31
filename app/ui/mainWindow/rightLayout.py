# app/ui/mainWindow/rightLayout.py

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel
from PyQt5.QtGui import QFont

def create_right_form_layout(vehicle_info):
    """Creates and returns the right form layout."""
    right_form_layout = QFormLayout()

    # Create text boxes and labels
    vehicle_info['rfidInputRight'] = QLineEdit()
    vehicle_info['vehicleNumberRight'] = QLineEdit()  # Ensure consistent naming
    vehicle_info['typeOfVehicleRight'] = QLineEdit()
    vehicle_info['validityTillRight'] = QLineEdit()
    vehicle_info['transporter'] = QLineEdit()
    vehicle_info['driverOwner'] = QLineEdit()
    vehicle_info['weighbridgeNo'] = QLineEdit()
    vehicle_info['doNumber'] = QLineEdit()
    vehicle_info['visitPurpose'] = QLineEdit()
    vehicle_info['placeToVisit'] = QLineEdit()
    vehicle_info['personToVisit'] = QLineEdit()
    vehicle_info['shift'] = QLineEdit()
    vehicle_info['section'] = QLineEdit()

    # Set properties for the text boxes
    text_boxes = [
        vehicle_info['rfidInputRight'], vehicle_info['vehicleNumberRight'], vehicle_info['typeOfVehicleRight'], vehicle_info['validityTillRight'],
        vehicle_info['transporter'], vehicle_info['driverOwner'], vehicle_info['weighbridgeNo'], vehicle_info['doNumber'],
        vehicle_info['visitPurpose'], vehicle_info['placeToVisit'], vehicle_info['personToVisit'], vehicle_info['shift'], vehicle_info['section']
    ]
    setup_text_boxes(text_boxes)

    # Set font size for labels
    label_font = QFont("Arial", 14)

    # Add labels and text boxes to the form layout
    right_form_layout.addRow(QLabel("RFID Tag:", font=label_font), vehicle_info['rfidInputRight'])
    right_form_layout.addRow(QLabel("Type of Vehicle:", font=label_font), vehicle_info['typeOfVehicleRight'])
    right_form_layout.addRow(QLabel("Vehicle No:", font=label_font), vehicle_info['vehicleNumberRight'])
    right_form_layout.addRow(QLabel("Validity Till:", font=label_font), vehicle_info['validityTillRight'])
    right_form_layout.addRow(QLabel("Do No:", font=label_font), vehicle_info['doNumber'])
    right_form_layout.addRow(QLabel("Transporter:", font=label_font), vehicle_info['transporter'])
    right_form_layout.addRow(QLabel("Driver:", font=label_font), vehicle_info['driverOwner'])
    right_form_layout.addRow(QLabel("Weighbridge No:", font=label_font), vehicle_info['weighbridgeNo'])
    right_form_layout.addRow(QLabel("Visit Purpose:", font=label_font), vehicle_info['visitPurpose'])
    right_form_layout.addRow(QLabel("Visit Place:", font=label_font), vehicle_info['placeToVisit'])
    right_form_layout.addRow(QLabel("Visit Person:", font=label_font), vehicle_info['personToVisit'])
    right_form_layout.addRow(QLabel("Shift:", font=label_font), vehicle_info['shift'])
    right_form_layout.addRow(QLabel("Section:", font=label_font), vehicle_info['section'])

    return right_form_layout

def setup_text_boxes(text_boxes):
    """Set properties for a list of text boxes."""
    text_box_width = 250  # Set a consistent width for all text boxes
    for text_box in text_boxes:
        text_box.setFixedWidth(text_box_width)
        text_box.setReadOnly(True)
