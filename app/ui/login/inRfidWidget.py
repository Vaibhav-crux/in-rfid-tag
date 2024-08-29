from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer
import os
from app.function.allotedTags.fetchAllotedTags import fetch_alloted_tag_by_rfid  # Import the function
from app.function.vehicleInOut.insertVehicleInOut import insert_vehicle_in_out_from_alloted_tag  # Import the insert function

class InRfidWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the timer before calling initUI
        self.timer = QTimer(self)  # Timer for auto-clear functionality
        self.timer.timeout.connect(self.clear_all_fields_and_file)  # Connect timer to clear function

        self.initUI()

    def initUI(self):
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignTop)  # Align to the top for a professional look

        stylesheet = 'app/stylesheet/login/lineEdit.qss'

        # Common width for all text boxes
        common_width = 200

        # Create each label and text box in the same row
        self.create_row(form_layout, 'RFID Tag:', 'rfid_entry', stylesheet, common_width)
        self.create_row(form_layout, 'Type of Vehicle:', 'vehicle_type_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Vehicle No:', 'vehicle_no_entry', stylesheet, common_width)
        self.create_row(form_layout, 'Validity Till:', 'validity_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Transporter:', 'transporter_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Driver/Owner:', 'driver_owner_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Weighbridge No:', 'weighbridge_no_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Visit Purpose:', 'visit_purpose_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Place to Visit:', 'place_to_visit_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Person to Visit:', 'person_to_visit_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Section:', 'section_entry', stylesheet, common_width, read_only=True)
        self.create_row(form_layout, 'Shift:', 'shift_entry', stylesheet, common_width, read_only=True)

        # Status Label
        self.status_label = QLabel('', self)
        self.status_label.setFont(QFont('Arial', 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.status_label)

        # Create a horizontal layout for the indicator to align it to the bottom right
        indicator_layout = QHBoxLayout()
        indicator_layout.addStretch()  # Push the indicator to the right

        # Indicator Label for Vehicle Status
        self.indicator_label = QLabel(self)
        self.indicator_label.setFixedSize(20, 20)  # Small circle indicator
        self.indicator_label.setStyleSheet("background-color: grey; border-radius: 10px;")  # Default to grey
        indicator_layout.addWidget(self.indicator_label, alignment=Qt.AlignRight)

        form_layout.addLayout(indicator_layout)

        self.setLayout(form_layout)
        self.load_rfid_from_file()

        # Connect Enter key press events
        self.rfid_entry.returnPressed.connect(self.focus_vehicle_type_entry)

    def create_row(self, layout, label_text, entry_attr, stylesheet, common_width, read_only=False):
        """Utility function to create a label and a line edit entry on the same row."""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(5)  # Minimal spacing between label and input
        label = QLabel(label_text, self)
        label.setFont(QFont('Arial', 14))  # Standard font size for readability
        entry = QLineEdit(self)
        entry.setFixedHeight(28)  # Standardized height
        entry.setFixedWidth(common_width)  # Set fixed width for all text boxes
        entry.setStyleSheet(self.load_stylesheet(stylesheet))
        if read_only:
            entry.setReadOnly(True)  # Make the entry read-only if specified
        setattr(self, entry_attr, entry)  # Dynamically set the attribute
        row_layout.addWidget(label)
        row_layout.addWidget(entry)
        row_layout.addStretch()  # Push everything to the left
        layout.addLayout(row_layout)

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
                self.fetch_vehicle_details()

    def fetch_vehicle_details(self):
        """Fetch vehicle details from the database based on the RFID tag."""
        rfid_tag = self.rfid_entry.text().strip()

        if rfid_tag:
            tag_details = fetch_alloted_tag_by_rfid(rfid_tag)
            if tag_details:
                # Populate fields
                self.vehicle_type_entry.setText(tag_details['typeOfVehicle'])
                self.vehicle_no_entry.setText(tag_details['vehicleNumber'])

                if tag_details.get('isRegistered', False):
                    # If vehicle is registered, populate all additional fields
                    self.validity_entry.setText(tag_details.get('validityTill', ''))
                    self.transporter_entry.setText(tag_details.get('transporter', ''))
                    self.driver_owner_entry.setText(tag_details.get('driverOwner', ''))
                    self.weighbridge_no_entry.setText(tag_details.get('weighbridgeNo', ''))
                    self.visit_purpose_entry.setText(tag_details.get('visitPurpose', ''))
                    self.place_to_visit_entry.setText(tag_details.get('placeToVisit', ''))
                    self.person_to_visit_entry.setText(tag_details.get('personToVisit', ''))
                    self.section_entry.setText(tag_details.get('section', ''))
                    self.shift_entry.setText(tag_details.get('shift', ''))
                    self.update_status("Vehicle Found", QColor(100, 149, 237))  # Green color for success
                    try:
                        insert_vehicle_in_out_from_alloted_tag(tag_details)
                        self.update_indicator("green")  # Update to green after successful insertion
                    except Exception as e:
                        # If insertion fails, set the indicator to red
                        print(f"Insertion failed: {e}")
                        self.update_indicator("red")
                else:
                    # Vehicle found in AllotedTags but not in VehicleRegistration
                    self.clear_additional_fields()
                    self.update_status("Vehicle Not Registered", QColor(255, 165, 0))  # Orange color
                    self.update_indicator("yellow")  # Update to yellow

            else:
                # Vehicle not found
                self.clear_all_fields()
                self.update_status("Vehicle Not Found", QColor(255, 0, 0))  # Red color
                self.update_indicator("red")  # Update to red

            # Start the timer to clear fields and file after 5 seconds
            self.timer.start(5000)
        else:
            # No RFID tag in the input field
            self.update_indicator("grey")  # Update to grey

    def clear_all_fields(self):
        """Clear all input fields, including the RFID Tag."""
        fields = [
            self.rfid_entry,  # Include the RFID entry field
            self.vehicle_type_entry, self.vehicle_no_entry, self.validity_entry,
            self.transporter_entry, self.driver_owner_entry, self.weighbridge_no_entry,
            self.visit_purpose_entry, self.place_to_visit_entry, self.person_to_visit_entry,
            self.section_entry, self.shift_entry
        ]
        for field in fields:
            field.clear()

    def clear_additional_fields(self):
        """Clear additional fields when vehicle is not registered."""
        fields = [
            self.validity_entry, self.transporter_entry, self.driver_owner_entry,
            self.weighbridge_no_entry, self.visit_purpose_entry, self.place_to_visit_entry,
            self.person_to_visit_entry, self.section_entry, self.shift_entry
        ]
        for field in fields:
            field.clear()

    def clear_all_fields_and_file(self):
        """Clear all input fields and the content of the text file."""
        self.clear_all_fields()

        # Clear the text in the file
        file_path = 'app/file/rfidFile.txt'
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('')  # Clear the file by writing an empty string

        self.update_status("Cleared", QColor(255, 0, 0))  # Update status to indicate clearing
        self.update_indicator("grey")  # Reset indicator to grey
        self.timer.stop()  # Stop the timer after clearing

    def update_status(self, message, color):
        """Update the status label with a message and color."""
        self.status_label.setText(f"Status: {message}")
        self.status_label.setStyleSheet(f"color: {color.name()}")

    def update_indicator(self, color):
        """Update the color of the indicator label."""
        color_map = {
            "green": "background-color: green; border-radius: 10px;",
            "yellow": "background-color: yellow; border-radius: 10px;",
            "red": "background-color: red; border-radius: 10px;",
            "grey": "background-color: grey; border-radius: 10px;"
        }
        self.indicator_label.setStyleSheet(color_map[color])

    def focus_vehicle_type_entry(self):
        """Move focus to the vehicle type entry when Enter is pressed in the RFID entry."""
        self.vehicle_type_entry.setFocus()
