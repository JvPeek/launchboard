import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from constants import COLOR_VALUES

class ButtonSettingsWidget(QWidget):
    def __init__(self, button, parent=None):
        super().__init__(parent)
        self.button = button
        self.parent_window = parent

        layout = QFormLayout()

        self.key_edit = QLineEdit(self)
        self.key_edit.setText(self.button.text() if self.button.text() != 'None' else '')
        self.key_edit.textChanged.connect(self.update_button_key)
        layout.addRow("Key:", self.key_edit)

        self.red_combo = QComboBox(self)
        self.green_combo = QComboBox(self)
        for i in range(4):
            self.red_combo.addItem(str(i))
            self.green_combo.addItem(str(i))

        self.red_combo.setCurrentIndex(self.get_color_index('red'))
        self.green_combo.setCurrentIndex(self.get_color_index('green'))

        self.red_combo.currentIndexChanged.connect(self.change_color)
        self.green_combo.currentIndexChanged.connect(self.change_color)
        layout.addRow("Red Value:", self.red_combo)
        layout.addRow("Green Value:", self.green_combo)

        # Add copy and paste buttons
        button_layout = QHBoxLayout()
        copy_button = QPushButton("Copy")
        paste_button = QPushButton("Paste")
        copy_button.clicked.connect(self.copy_settings)
        paste_button.clicked.connect(self.paste_settings)
        button_layout.addWidget(copy_button)
        button_layout.addWidget(paste_button)
        layout.addRow(button_layout)

        self.setLayout(layout)

        # Add keyboard shortcuts
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(self.copy_settings)
        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(self.paste_settings)

    def update_button_key(self, text):
        self.button.setText(text if text else 'None')

    def get_color_index(self, color):
        button_color = self.button.styleSheet().split('; ')[0].split(': ')[-1][:-1] if self.button.styleSheet() else "#000000"
        if color == 'red':
            red_hex = button_color[1:3]
            return list(COLOR_VALUES.values()).index(red_hex) if red_hex in COLOR_VALUES.values() else 0
        elif color == 'green':
            green_hex = button_color[3:5]
            return list(COLOR_VALUES.values()).index(green_hex) if green_hex in COLOR_VALUES.values() else 0

    def change_color(self):
        red_value = COLOR_VALUES[int(self.red_combo.currentText())]
        green_value = COLOR_VALUES[int(self.green_combo.currentText())]
        color = f"#{red_value}{green_value}00"
        self.button.setStyleSheet(f"background-color: {color}")

    def copy_settings(self):
        settings = {
            'key': self.key_edit.text(),
            'r': int(self.red_combo.currentText()),
            'g': int(self.green_combo.currentText())
        }
        clipboard = QApplication.clipboard()
        clipboard.setText(json.dumps(settings))

    def paste_settings(self):
        clipboard = QApplication.clipboard()
        settings = clipboard.text()
        try:
            settings = json.loads(settings)
            self.key_edit.setText(settings['key'])
            self.red_combo.setCurrentIndex(settings['r'])
            self.green_combo.setCurrentIndex(settings['g'])
        except (json.JSONDecodeError, KeyError):
            QMessageBox.warning(self, "Error", "Invalid clipboard data")
