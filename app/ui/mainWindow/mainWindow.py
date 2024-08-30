import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from .title_bar import create_title_bar
from .image_label import create_image_label
from .timeSection import create_clock_frame
from .fetchDataFromFile import fetch_and_update_rfid  # Import the fetch function

class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.rfid_input_left = None
        self.rfid_input_right = None
        self.status_label = None
        self.indicator_label = None
        self.vehicle_info = {}
        self.setup_ui()

    def load_stylesheet(self, file_path):
        """Utility function to load and return a stylesheet."""
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Stylesheet file not found: {file_path}")
            return ""

    def setup_ui(self):
        """Main UI setup method."""
        # Apply the stylesheet
        stylesheet = self.load_stylesheet("app/stylesheet/mainWindow/mainWindow.qss")
        self.setStyleSheet(stylesheet)

        # Remove the default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()

        # Main layout with margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)  # Add margins: left, top, right, bottom
        main_layout.setSpacing(10)  # Add spacing between elements
        self.setLayout(main_layout)  # Set the layout for the window

        # Create custom title bar and add to layout
        title_bar_frame = create_title_bar(self)
        main_layout.addWidget(title_bar_frame)

        # Create the content layout
        content_layout = self.create_content_layout()
        main_layout.addLayout(content_layout)

        # After the window is fully loaded, update the RFID Tag
        QTimer.singleShot(1000, self.update_rfid_tag)  # Delay to ensure everything is loaded

    def create_content_layout(self):
        """Creates and returns the main content layout."""
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)  # Increase spacing between elements

        # Create and add the left form layout
        left_form_layout = self.create_left_form_layout()
        content_layout.addLayout(left_form_layout)

        # Add a vertical separator
        separator1 = self.create_separator()
        content_layout.addWidget(separator1)

        # Create and add the right form layout
        right_form_layout = self.create_right_form_layout()
        content_layout.addLayout(right_form_layout)

        # Add another vertical separator
        separator2 = self.create_separator()
        content_layout.addWidget(separator2)

        # Create and add the image and clock layout
        image_clock_layout = self.create_image_clock_layout()
        content_layout.addLayout(image_clock_layout)

        return content_layout

    def create_left_form_layout(self):
        """Creates and returns the left form layout."""
        left_form_layout = QFormLayout()

        # Create text boxes and labels
        self.rfid_input_left = QLineEdit()
        vehicle_no_input_left = QLineEdit()
        vehicle_type_input_left = QLineEdit()
        validity_till_input_left = QLineEdit()

        # Set properties for the text boxes
        text_boxes = [self.rfid_input_left, vehicle_no_input_left, vehicle_type_input_left, validity_till_input_left]
        self.setup_text_boxes(text_boxes)

        # Store vehicle information text boxes in a dictionary for easy access
        self.vehicle_info.update({
            'typeOfVehicleLeft': vehicle_type_input_left,
            'vehicleNumberLeft': vehicle_no_input_left,
            'validityTillLeft': validity_till_input_left,
        })

        # Set font size for labels
        label_font = QFont("Arial", 14)

        # Add labels and text boxes to the form layout
        left_form_layout.addRow(QLabel("RFID Tag:", font=label_font), self.rfid_input_left)
        left_form_layout.addRow(QLabel("Vehicle No:", font=label_font), vehicle_no_input_left)
        left_form_layout.addRow(QLabel("Type of Vehicle:", font=label_font), vehicle_type_input_left)
        left_form_layout.addRow(QLabel("Validity Till:", font=label_font), validity_till_input_left)

        # Add the status frame
        status_frame = self.create_status_frame()
        left_form_layout.addRow(QLabel(""))  # Add empty rows for spacing
        left_form_layout.addRow(QLabel(""))
        left_form_layout.addRow(status_frame)

        return left_form_layout

    def create_right_form_layout(self):
        """Creates and returns the right form layout."""
        right_form_layout = QFormLayout()

        # Create text boxes and labels
        self.rfid_input_right = QLineEdit()
        vehicle_no_input_right = QLineEdit()
        vehicle_type_input_right = QLineEdit()
        validity_till_input_right = QLineEdit()
        transporter_input = QLineEdit()
        driver_input = QLineEdit()
        weighbridge_no_input = QLineEdit()
        challan_no_input = QLineEdit()
        visit_purpose_input = QLineEdit()
        visit_place_input = QLineEdit()
        visit_person_input = QLineEdit()
        shift_input = QLineEdit()
        section_input = QLineEdit()

        # Set properties for the text boxes
        text_boxes = [
            self.rfid_input_right, vehicle_no_input_right, vehicle_type_input_right, validity_till_input_right,
            transporter_input, driver_input, weighbridge_no_input, challan_no_input,
            visit_purpose_input, visit_place_input, visit_person_input, shift_input, section_input
        ]
        self.setup_text_boxes(text_boxes)

        # Store vehicle information text boxes in a dictionary for easy access
        self.vehicle_info.update({
            'typeOfVehicleRight': vehicle_type_input_right,
            'vehicleNumberRight': vehicle_no_input_right,
            'doNumber': challan_no_input,
            'transporter': transporter_input,
            'driverOwner': driver_input,
            'weighbridgeNo': weighbridge_no_input,
            'visitPurpose': visit_purpose_input,
            'placeToVisit': visit_place_input,
            'personToVisit': visit_person_input,
            'validityTillRight': validity_till_input_right,
            'section': section_input,
            'shift': shift_input,
        })

        # Set font size for labels
        label_font = QFont("Arial", 14)

        # Add labels and text boxes to the form layout
        right_form_layout.addRow(QLabel("RFID Tag:", font=label_font), self.rfid_input_right)
        right_form_layout.addRow(QLabel("Vehicle No:", font=label_font), vehicle_no_input_right)
        right_form_layout.addRow(QLabel("Type of Vehicle:", font=label_font), vehicle_type_input_right)
        right_form_layout.addRow(QLabel("Validity Till:", font=label_font), validity_till_input_right)
        right_form_layout.addRow(QLabel("Transporter:", font=label_font), transporter_input)
        right_form_layout.addRow(QLabel("Driver:", font=label_font), driver_input)
        right_form_layout.addRow(QLabel("Weighbridge No:", font=label_font), weighbridge_no_input)
        right_form_layout.addRow(QLabel("Challan No:", font=label_font), challan_no_input)
        right_form_layout.addRow(QLabel("Visit Purpose:", font=label_font), visit_purpose_input)
        right_form_layout.addRow(QLabel("Visit Place:", font=label_font), visit_place_input)
        right_form_layout.addRow(QLabel("Visit Person:", font=label_font), visit_person_input)
        right_form_layout.addRow(QLabel("Shift:", font=label_font), shift_input)
        right_form_layout.addRow(QLabel("Section:", font=label_font), section_input)

        return right_form_layout

    def create_image_clock_layout(self):
        """Creates and returns the image and clock layout."""
        image_clock_layout = QVBoxLayout()
        image_clock_layout.setSpacing(10)  # Add spacing between the image and clock

        # Add the image label
        image_label = create_image_label(self)
        image_label.setFixedSize(250, 200)  # Set size for the image
        image_clock_layout.addWidget(image_label, 0, Qt.AlignCenter)

        # Create and add the digital clock frame using the imported function
        clock_frame = create_clock_frame(self)
        image_clock_layout.addWidget(clock_frame, 0, Qt.AlignCenter)

        return image_clock_layout

    def create_status_frame(self):
        """Creates and returns the status frame."""
        status_frame = QFrame(self)
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 18px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(10, 10, 10, 10)

        # Status label (inside the frame)
        self.status_label = QLabel("Waiting")
        self.status_label.setFont(QFont("Arial", 16, QFont.Bold))
        status_layout.addWidget(self.status_label, alignment=Qt.AlignLeft)

        # Indicator label
        self.indicator_label = QLabel()
        self.indicator_label.setFixedSize(20, 20)
        self.indicator_label.setStyleSheet("background-color: grey; border-radius: 10px;")
        status_layout.addWidget(self.indicator_label)

        status_layout.addStretch()  # Add stretch to push content to the left

        return status_frame

    def setup_text_boxes(self, text_boxes):
        """Set properties for a list of text boxes."""
        text_box_width = 250  # Set a consistent width for all text boxes
        for text_box in text_boxes:
            text_box.setFixedWidth(text_box_width)
            text_box.setReadOnly(True)

    def create_separator(self):
        """Creates and returns a vertical separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #2c3e50;")
        return separator

    def update_rfid_tag(self):
        """Fetches the RFID tag from the file and updates the text boxes."""
        fetch_and_update_rfid(
            "app/file/readVehicle.txt", 
            self.rfid_input_left, 
            self.rfid_input_right, 
            self.status_label, 
            self.indicator_label,
            self.vehicle_info,
            self  # Pass the window instance
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
