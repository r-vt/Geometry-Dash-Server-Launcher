import os
import json
import sys
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
import random

number = random.randint(0, 5)

config_folder = os.path.join(os.getcwd(), 'gd_config')
config_file = os.path.join(config_folder, 'config.json')

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def save_config(config_data):
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)

def search_for_geometry_dash():
    steam_paths = [
        os.path.join(os.getenv('ProgramFiles(x86)'), 'Steam', 'steamapps', 'common'),
        os.path.join(os.getenv('ProgramFiles'), 'Steam', 'steamapps', 'common'),
        os.path.join(os.getenv('ProgramFiles'), 'SteamLibrary', 'steamapps', 'common'),
        os.path.join(os.getenv('ProgramFiles(x86)'), 'SteamLibrary', 'steamapps', 'common')
    ]

    for path in steam_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if 'GeometryDash.exe' in files:
                    return os.path.join(root, 'GeometryDash.exe')
    return None

def restart_program():
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()

def load_custom_font(font_path):
    font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
    font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        return font_families[0]
    return None

class ServerSelectionWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Server")
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: #f0f4ff; border-radius: 15px;")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.info_label = QtWidgets.QLabel("Select a server to launch")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #333; font-size: 27px; background: transparent;")
        self.layout.addWidget(self.info_label)

        self.server_buttons_layout = QtWidgets.QVBoxLayout()

        self.config_data = load_config()
        for server_name in self.config_data.keys():
            button = QtWidgets.QPushButton(server_name)
            button.setStyleSheet(self.get_button_style())
            button.clicked.connect(lambda checked, name=server_name: self.server_selected(name))
            self.server_buttons_layout.addWidget(button)

        self.layout.addLayout(self.server_buttons_layout)
        self.setLayout(self.layout)

    def server_selected(self, server_name):
        self.parent().set_selected_server(server_name)
        self.accept()

    def get_button_style(self):
        return (
            "QPushButton {"
            "background-color: #182452; color: white; font-size: 21px; padding: 7.5px 15px; border-radius: 12px;"
            "border: none;}"
            "QPushButton:hover {"
            "background-color: #263880;"
            "}"
        )

class GeometryDashLauncher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometry Dash Server Launcher")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f4ff; border-radius: 15px;")

        self.background_label = QtWidgets.QLabel(self)
        if number == 5:
            self.background_pixmap = QtGui.QPixmap("assets/background2.png")
        else:
            self.background_pixmap = QtGui.QPixmap("assets/background.png")
        self.background_label.setPixmap(self.background_pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.rect())

        self.logo_label = QtWidgets.QLabel(self)
        self.logo_pixmap = QtGui.QPixmap("assets/textfont.png")
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent;")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.logo_label)

        self.layout.setContentsMargins(20, 20, 20, 20)

        button_layout = QtWidgets.QHBoxLayout()
        self.add_instance_button = self.create_button("Add New Server")
        self.server_button = self.create_button("Choose Server")

        button_layout.addWidget(self.add_instance_button)
        button_layout.addWidget(self.server_button)

        self.layout.addLayout(button_layout)

        self.selected_instance_label = QtWidgets.QLabel("Selected Server: None")
        self.selected_instance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.selected_instance_label.setStyleSheet("color: #333; font-size: 27px; background: transparent;")
        self.layout.addWidget(self.selected_instance_label)

        self.launch_button = QtWidgets.QPushButton("Launch")
        self.launch_button.setStyleSheet(self.get_launch_button_style())
        self.launch_button.setFixedSize(300, 75)
        self.launch_button.clicked.connect(self.run_selected_instance)
        self.layout.addWidget(self.launch_button, alignment=QtCore.Qt.AlignCenter)

        self.footer_layout = QtWidgets.QHBoxLayout()
        self.exit_on_launch_checkbox = QtWidgets.QCheckBox("Exit when launching")
        self.exit_on_launch_checkbox.setStyleSheet(
            "QCheckBox { color: #333; font-size: 21px; }"
            "QCheckBox::indicator { width: 20px; height: 20px; }"
            "QCheckBox::indicator:unchecked { background-color: #333; border-radius: 5px; }"
            "QCheckBox::indicator:checked { background-color: #367691; border-radius: 5px; }"
        )
        self.footer_label = QtWidgets.QLabel("Made by RVT\nVersion 1.0 | Windows Build")
        self.footer_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.footer_label.setStyleSheet("color: #666; font-size: 18px; background: transparent;")
        
        self.footer_layout.addWidget(self.footer_label)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.exit_on_launch_checkbox)
        
        self.layout.addLayout(self.footer_layout)

        self.setLayout(self.layout)
        self.auto_check_for_original_instance()

        self.selected_instance = None

        self.set_font()

    def set_font(self):
        font_path = "assets/PUSAB.otf"
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font = QtGui.QFont(font_families[0])
            self.setFont(font)
            for widget in self.findChildren(QtWidgets.QWidget):
                widget.setFont(font)

    def create_button(self, text):
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet(self.get_button_style())
        button.setFixedSize(225, 60)

        button.clicked.connect(self.add_instance if text == "Add New Server" else self.show_server_menu)
        return button

    def get_button_style(self):
        return (
            "QPushButton {"
            "background-color: #182452; color: white; font-size: 21px; padding: 7.5px 15px; border-radius: 12px;"
            "border: none;}"
            "QPushButton:hover {"
            "background-color: #263880;"
            "}"
        )

    def get_launch_button_style(self):
        return (
            "QPushButton {"
            "background-color: #367691; color: white; font-size: 27px; padding: 15px 30px; border-radius: 15px;"
            "border: none;}"
            "QPushButton:hover {"
            "background-color: #4699bd;"
            "}"
        )

    def resizeEvent(self, event):
        self.background_label.setGeometry(self.rect())
        self.logo_label.setGeometry((self.width() - self.logo_pixmap.width()) // 2, 20, self.logo_pixmap.width(), self.logo_pixmap.height())
        super().resizeEvent(event)

    def auto_check_for_original_instance(self):
        config_data = load_config()
        if "Geometry Dash" not in config_data:
            exe_path = search_for_geometry_dash()
            if exe_path:
                folder_path = os.path.dirname(exe_path)
                config_data["Geometry Dash"] = {
                    "folder_path": folder_path,
                    "exe_path": exe_path
                }
                save_config(config_data)

    def add_instance(self):
        instance_name, ok = QtWidgets.QInputDialog.getText(self, "New Server", "Enter instance name:")
        if not ok or not instance_name:
            return

        exe_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select the server's executable", "", "Executable Files (*.exe)")
        if exe_path:
            folder_path = os.path.dirname(exe_path)
            config_data = load_config()
            config_data[instance_name] = {
                "folder_path": folder_path,
                "exe_path": exe_path
            }
            save_config(config_data)
            restart_program()

    def show_server_menu(self):
        server_selection_window = ServerSelectionWindow(self)
        server_selection_window.exec_()

    def set_selected_server(self, server_name):
        self.selected_instance = server_name
        self.selected_instance_label.setText(f"Selected Server: {server_name}")

    def run_selected_instance(self):
        if self.selected_instance:
            config_data = load_config()
            server_data = config_data.get(self.selected_instance)
            if server_data:
                folder_path = server_data['folder_path']
                exe_path = server_data['exe_path']
                os.chdir(folder_path)
                subprocess.Popen(exe_path)
                if self.exit_on_launch_checkbox.isChecked():
                    sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = GeometryDashLauncher()
    launcher.show()
    sys.exit(app.exec_())
