import sys
from PyQt5.QtWidgets import QApplication
from app.ui.theme.theme import set_dark_mode, set_light_mode
from app.ui.login.login import LoginWindow
from app.config.db_config import init_db

def start_app():
    app = QApplication(sys.argv)

    # Choose the mode (dark or light)
    mode = 'dark'  # Change to 'light' to use light mode
    if mode == 'dark':
        set_dark_mode(app)
    else:
        set_light_mode(app)

    # Initialize the database
    init_db()

    # Launch the login window
    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())

def main():
    start_app()

if __name__ == '__main__':
    main()
