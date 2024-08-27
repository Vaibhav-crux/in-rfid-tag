from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import os
from app.function.allotedTags.fetchAllotedTags import fetch_alloted_tag_by_rfid  # Import the function
from app.function.vehicleInOut.insertVehicleInOut import insert_vehicle_in_out_from_alloted_tag  # Import the insert function

class InRfidWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        stylesheet = 'app/stylesheet/login/lineEdit.qss'

        # RFID Tag
        rfid_label = QLabel('RFID Tag:', self)
        rfid_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.rfid_entry = QLineEdit(self)
        self.rfid_entry.setFixedHeight(35)
        self.rfid_entry.setStyleSheet(self.load_stylesheet(stylesheet))
        self.rfid_entry.setPlaceholderText("RFID Tag")
        self.rfid_entry.editingFinished.connect(self.fetch_vehicle_details)  # Trigger when editing is finished

        # Vehicle Type
        vehicle_type_label = QLabel('Type of Vehicle:', self)
        vehicle_type_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.vehicle_type_entry = QLineEdit(self)
        self.vehicle_type_entry.setFixedHeight(35)
        self.vehicle_type_entry.setStyleSheet(self.load_stylesheet(stylesheet))
        self.vehicle_type_entry.setPlaceholderText("Type of Vehicle")

        # Vehicle No
        vehicle_no_label = QLabel('Vehicle No:', self)
        vehicle_no_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.vehicle_no_entry = QLineEdit(self)
        self.vehicle_no_entry.setFixedHeight(35)
        self.vehicle_no_entry.setStyleSheet(self.load_stylesheet(stylesheet))
        self.vehicle_no_entry.setPlaceholderText("Vehicle No")

        # Validity Till
        validity_label = QLabel('Validity Till:', self)
        validity_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.validity_entry = QLineEdit(self)
        self.validity_entry.setFixedHeight(35)
        self.validity_entry.setStyleSheet(self.load_stylesheet(stylesheet))
        self.validity_entry.setPlaceholderText("Validity Till")

        # Status Label
        self.status_label = QLabel('', self)
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setAlignment(Qt.AlignCenter)

        # Arrange the widgets in the form layout
        form_layout.addWidget(rfid_label)
        form_layout.addWidget(self.rfid_entry)
        form_layout.addWidget(vehicle_type_label)
        form_layout.addWidget(self.vehicle_type_entry)
        form_layout.addWidget(vehicle_no_label)
        form_layout.addWidget(self.vehicle_no_entry)
        form_layout.addWidget(validity_label)
        form_layout.addWidget(self.validity_entry)
        form_layout.addWidget(self.status_label)  # Add status label below the validity entry

        self.setLayout(form_layout)

        # Load the RFID value from the file and set it in the rfid_entry after all widgets are initialized
        self.load_rfid_from_file()

        # Connect Enter key press events
        self.rfid_entry.returnPressed.connect(self.focus_vehicle_type_entry)
        self.vehicle_type_entry.returnPressed.connect(self.focus_vehicle_no_entry)
        self.vehicle_no_entry.returnPressed.connect(self.focus_validity_entry)

    def load_stylesheet(self, file_path):
        """Utility function to load and return a stylesheet."""
        with open(file_path, "r") as file:
            return file.read()

    def load_rfid_from_file(self):
        """Load RFID value from the file and set it in the rfid_entry."""
        file_path = 'app/file/rfidFile.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                rfid_value = file.read().strip()
                self.rfid_entry.setText(rfid_value)
                self.fetch_vehicle_details()  # Fetch details after loading RFID from file

    def fetch_vehicle_details(self):
        """Fetch vehicle details from the database based on the RFID tag."""
        rfid_tag = self.rfid_entry.text().strip()

        if rfid_tag:
            tag_details = fetch_alloted_tag_by_rfid(rfid_tag)
            if tag_details:
                # Populate fields
                self.vehicle_type_entry.setText(tag_details['typeOfVehicle'])
                self.vehicle_no_entry.setText(tag_details['vehicleNumber'])
                self.validity_entry.setText(tag_details['validityTill'])
                self.update_status("Vehicle Found", QColor(100, 149, 237))  # Green color for success

                # Insert into VehicleInOut table
                insert_vehicle_in_out_from_alloted_tag(tag_details)
            else:
                # Clear the fields if no entry is found
                self.vehicle_type_entry.clear()
                self.vehicle_no_entry.clear()
                self.validity_entry.clear()
                self.update_status("Vehicle Not Found", QColor(255, 0, 0))  # Red color for failure

    def update_status(self, message, color):
        """Update the status label with a message and color."""
        self.status_label.setText(f"Status: {message}")
        self.status_label.setStyleSheet(f"color: {color.name()}")

    def focus_vehicle_type_entry(self):
        """Move focus to the vehicle type entry when Enter is pressed in the RFID entry."""
        self.vehicle_type_entry.setFocus()

    def focus_vehicle_no_entry(self):
        """Move focus to the vehicle no entry when Enter is pressed in the vehicle type entry."""
        self.vehicle_no_entry.setFocus()

    def focus_validity_entry(self):
        """Move focus to the validity entry when Enter is pressed in the vehicle no entry."""
        self.validity_entry.setFocus()
