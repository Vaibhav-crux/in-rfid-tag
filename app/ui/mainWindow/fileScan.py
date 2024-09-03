import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

class FileScanDialog(QDialog):
    def __init__(self, parent=None, vehicle_info=None):
        super().__init__(parent)
        self.vehicle_info = vehicle_info  # Pass vehicle_info to access RFID field
        self.setWindowTitle("File Options")
        self.setFixedSize(300, 150)  # Set the size of the dialog
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components of the dialog."""
        layout = QVBoxLayout(self)

        # ComboBox with file options
        self.combo_box = QComboBox(self)
        self.populate_combobox_with_files()  # Populate ComboBox with file names
        layout.addWidget(QLabel("Select a file:", self))
        layout.addWidget(self.combo_box)

        # Create a horizontal layout for Save and Cancel buttons
        button_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_action)
        button_layout.addWidget(save_button)

        # Cancel button
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)  # Close the dialog
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def populate_combobox_with_files(self):
        """Populate the ComboBox with file names from the specified directory."""
        directory_path = "app/utils/rfidFile"  # Specify the directory
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            files = os.listdir(directory_path)
            rfid_files = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]
            self.combo_box.addItems(rfid_files)  # Add file names to the ComboBox
        else:
            self.combo_box.addItem("No files found")

    def save_action(self):
        """Action to perform when Save button is clicked."""
        selected_file = self.combo_box.currentText()
        directory_path = "app/utils/rfidFile"
        file_path = os.path.join(directory_path, selected_file)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    # Update the RFID Tag TextBox in the left frame
                    if self.vehicle_info and 'rfidInputLeft' in self.vehicle_info:
                        self.vehicle_info['rfidInputLeft'].setText(file_content)
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
        else:
            print("The selected file could not be found.")

        self.accept()  # Close the dialog after the action

def open_file_scan_dialog(parent, vehicle_info):
    """Function to open the FileScanDialog."""
    dialog = FileScanDialog(parent, vehicle_info=vehicle_info)
    dialog.exec_()
