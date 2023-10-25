import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog
from PyQt5.QtGui import QPalette, QColor, QTextCursor, QTextCharFormat, QFont, QIcon

import subprocess
import psutil

class EditServerPropertiesDialog(QDialog):
    def __init__(self, server_properties_content):
        super().__init__()
        self.server_properties_content = server_properties_content
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit server.properties")
        self.setGeometry(400, 400, 500, 500)

        layout = QVBoxLayout()

        # Create a QTextEdit widget for editing server.properties
        self.server_properties_edit = QTextEdit()
        self.server_properties_edit.setPlainText(self.server_properties_content)
        self.server_properties_edit.setAutoFillBackground(False)

        # Create a Save button for server.properties editing
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_server_properties)

        layout.addWidget(self.server_properties_edit)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_server_properties(self):
        # Save the changes made to the server.properties file
        content = self.server_properties_edit.toPlainText()
        try:
            with open("server.properties", "w") as file:
                file.write(content)
            self.accept()  # Close the dialog
        except Exception as e:
            self.show_error_popup(f"Error saving server.properties: {str(e)}")

    def show_error_popup(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

class MinecraftServerHelperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the background color to black with white text
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(dark_palette)

        self.setWindowTitle("Minecraft Server Helper")
        self.setGeometry(300, 300, 800, 800)  # Centered on the screen

        # Set the application icon
        self.setWindowIcon(QIcon("icon.ico"))

        layout = QVBoxLayout()

        # Get the public internet IP using the requests library
        public_ip = self.get_public_ip()

        # Use QTextEdit for IP and port, set as read-only
        self.ip_textedit = QTextEdit()
        self.ip_textedit.setPlainText(f"Server IP: {public_ip}\nServer Port: 25526")
        self.ip_textedit.setAlignment(Qt.AlignCenter)
        self.ip_textedit.setReadOnly(True)
        self.ip_textedit.viewport().setAutoFillBackground(False)
        self.ip_textedit.setStyleSheet("background-color: black; color: white;")

        # Set the text size to be larger
        text_format = QTextCharFormat()
        text_format.setFontPointSize(16)
        text_format.setForeground(QColor(255, 255, 255))
        cursor = self.ip_textedit.textCursor()
        cursor.setPosition(0)
        cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(text_format)
        cursor.clearSelection()

        self.start_button = QPushButton("Start Server")
        self.start_button.setStyleSheet("background-color: green;")
        self.start_button.clicked.connect(self.start_server)

        self.stop_button = QPushButton("Stop Server")
        self.stop_button.setStyleSheet("background-color: red;")
        self.stop_button.clicked.connect(self.stop_server)

        self.edit_button = QPushButton("Edit server.properties")
        self.edit_button.clicked.connect(self.edit_server_properties)

        layout.addWidget(self.ip_textedit)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.edit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_public_ip(self):
        try:
            response = requests.get("https://api.ipify.org")
            return response.text
        except requests.RequestException as e:
            self.show_error_popup(f"Error getting public IP: {str(e)}")
            return "Error"

    def start_server(self):
        try:
            subprocess.Popen(["start", "mcstart.bat"], shell=True)
        except FileNotFoundError:
            self.show_error_popup("mcstart.bat not found. Please provide the correct path to the Minecraft server start batch file.")

    def stop_server(self):
        try:
            subprocess.run(["taskkill", "/f", "/im", "java.exe"])
        except FileNotFoundError:
            self.show_error_popup("taskkill command not found. Ensure you are using Windows.")
        except subprocess.CalledProcessError:
            self.show_error_popup("Failed to stop the server.")
        else:
            print("Server stopped successfully.")

    def edit_server_properties(self):
        # Read the existing server.properties file, if it exists
        try:
            with open("server.properties", "r") as file:
                server_properties_content = file.read()
        except FileNotFoundError:
            self.show_error_popup("server.properties file not found. Please provide the correct path.")
            return

        # Open the server.properties editing dialog
        dialog = EditServerPropertiesDialog(server_properties_content)
        dialog.exec_()  # Display the dialog

    def show_error_popup(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = MinecraftServerHelperGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
