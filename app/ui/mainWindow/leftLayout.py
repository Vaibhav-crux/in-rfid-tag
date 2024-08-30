# app/ui/mainWindow/leftLayout.py

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel
from PyQt5.QtGui import QFont
from .statusFrame import create_status_frame

def create_left_form_layout(vehicle_info):
    """Creates and returns the left form layout."""
    left_form_layout = QFormLayout()

    # Create text boxes and labels
    vehicle_info['rfidInputLeft'] = QLineEdit()
    vehicle_info['vehicleNumberLeft'] = QLineEdit()  # Ensure consistent naming
    vehicle_info['typeOfVehicleLeft'] = QLineEdit()
    vehicle_info['validityTillLeft'] = QLineEdit()

    # Set properties for the text boxes
    text_boxes = [vehicle_info['rfidInputLeft'], vehicle_info['vehicleNumberLeft'], vehicle_info['typeOfVehicleLeft'], vehicle_info['validityTillLeft']]
    setup_text_boxes(text_boxes)

    # Set font size for labels
    label_font = QFont("Arial", 14)

    # Add labels and text boxes to the form layout
    left_form_layout.addRow(QLabel("RFID Tag:", font=label_font), vehicle_info['rfidInputLeft'])
    left_form_layout.addRow(QLabel("Vehicle No:", font=label_font), vehicle_info['vehicleNumberLeft'])
    left_form_layout.addRow(QLabel("Type of Vehicle:", font=label_font), vehicle_info['typeOfVehicleLeft'])
    left_form_layout.addRow(QLabel("Validity Till:", font=label_font), vehicle_info['validityTillLeft'])

    # Add the status frame
    status_frame = create_status_frame(vehicle_info)
    left_form_layout.addRow(QLabel(""))  # Add empty rows for spacing
    left_form_layout.addRow(QLabel(""))
    left_form_layout.addRow(status_frame)

    return left_form_layout

def setup_text_boxes(text_boxes):
    """Set properties for a list of text boxes."""
    text_box_width = 250  # Set a consistent width for all text boxes
    for text_box in text_boxes:
        text_box.setFixedWidth(text_box_width)
        text_box.setReadOnly(True)
