import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QShortcut, QCheckBox
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

        self.key_enabled_checkbox = QCheckBox(self)
        self.key_enabled_checkbox.setChecked(self.button.property(
            'keyEnabled') if self.button.property('keyEnabled') is not None else False)
        self.key_enabled_checkbox.stateChanged.connect(
            self.update_button_property)
        self.key_enabled_checkbox.stateChanged.connect(self.toggle_key_field)
        layout.addRow("Emulate Key", self.key_enabled_checkbox)

        self.key_edit = QLineEdit(self)
        self.key_edit.setText(self.button.text())
        self.key_edit.textChanged.connect(self.update_button_property)
        layout.addRow("Key:", self.key_edit)

        self.mqtt_enabled_checkbox = QCheckBox(self)
        self.mqtt_enabled_checkbox.setChecked(self.button.property(
            'mqttEnabled') if self.button.property('mqttEnabled') is not None else False)
        self.mqtt_enabled_checkbox.stateChanged.connect(
            self.update_button_property)
        self.mqtt_enabled_checkbox.stateChanged.connect(
            self.toggle_mqtt_fields)
        layout.addRow("Send MQTT message", self.mqtt_enabled_checkbox)

        self.mqtt_message_edit = QLineEdit(self)
        self.mqtt_message_edit.textChanged.connect(self.update_button_property)
        self.mqtt_message_edit.setText(self.button.property(
            'mqttMessage') if self.button.property('mqttMessage') else '')
        layout.addRow("MQTT Message:", self.mqtt_message_edit)

        self.mqtt_topic_edit = QLineEdit(self)
        self.mqtt_topic_edit.textChanged.connect(self.update_button_property)
        self.mqtt_topic_edit.setText(self.button.property(
            'mqttTopic') if self.button.property('mqttTopic') else '')
        layout.addRow("MQTT Topic:", self.mqtt_topic_edit)

        self.sound_enabled_checkbox = QCheckBox(self)
        self.sound_enabled_checkbox.setChecked(self.button.property(
            'soundEnabled') if self.button.property('soundEnabled') is not None else False)
        self.sound_enabled_checkbox.stateChanged.connect(
            self.update_button_property)
        self.sound_enabled_checkbox.stateChanged.connect(
            self.toggle_sound_fields)
        layout.addRow("Play sound", self.sound_enabled_checkbox)

        self.sound_edit = QLineEdit(self)
        self.sound_edit.textChanged.connect(self.update_button_property)
        self.sound_edit.setText(self.button.property(
            'sound') if self.button.property('sound') else '')
        layout.addRow("Sound:", self.sound_edit)

        self.page_enabled_checkbox = QCheckBox(self)
        self.page_enabled_checkbox.setChecked(self.button.property(
            'pageEnabled') if self.button.property('pageEnabled') is not None else False)
        self.page_enabled_checkbox.stateChanged.connect(
            self.update_button_property)
        self.page_enabled_checkbox.stateChanged.connect(self.toggle_page_field)
        layout.addRow("Switch page", self.page_enabled_checkbox)

        self.page_combo = QComboBox(self)
        for i in range(1, 9):
            self.page_combo.addItem(f"Page {i}", i)
        self.page_combo.setCurrentIndex(self.get_page_index())

        self.page_combo.currentIndexChanged.connect(
            self.update_button_property)
        layout.addRow("Page:", self.page_combo)

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

        # Initialize the state of the input fields
        self.toggle_mqtt_fields()
        self.toggle_sound_fields()
        self.toggle_key_field()
        self.toggle_page_field()

    def get_color_index(self, color):
        button_color = self.button.styleSheet().split('; ')[0].split(
            ': ')[-1][:-1] if self.button.styleSheet() else "#000000"
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

    def get_page_index(self):
        page = self.button.property('page')
        return int(page) - 1 if page else 0

    def update_button_property(self):
        if hasattr(self, 'key_edit'):
            self.button.setText(self.key_edit.text())
            self.button.setProperty("key",self.key_edit.text())
        if hasattr(self, 'mqtt_enabled_checkbox'):
            self.button.setProperty('mqttEnabled', self.mqtt_enabled_checkbox.isChecked())
        if hasattr(self, 'mqtt_message_edit'):
            self.button.setProperty('mqttMessage', self.mqtt_message_edit.text())
        if hasattr(self, 'mqtt_topic_edit'):
            self.button.setProperty('mqttTopic', self.mqtt_topic_edit.text())
        if hasattr(self, 'sound_enabled_checkbox'):
            self.button.setProperty('soundEnabled', self.sound_enabled_checkbox.isChecked())
        if hasattr(self, 'sound_edit'):
            self.button.setProperty('sound', self.sound_edit.text())
        if hasattr(self, 'key_enabled_checkbox'):
            self.button.setProperty('keyEnabled', self.key_enabled_checkbox.isChecked())
        if hasattr(self, 'page_enabled_checkbox'):
            self.button.setProperty('pageEnabled', self.page_enabled_checkbox.isChecked())
        if hasattr(self, 'page_combo'):
            self.button.setProperty('page', self.page_combo.currentData())


    def copy_settings(self):
        settings = {
            'dataType': 'button',
            'key': self.key_edit.text(),
            'r': int(self.red_combo.currentText()),
            'g': int(self.green_combo.currentText()),
            'mqttEnabled': self.mqtt_enabled_checkbox.isChecked(),
            'mqttMessage': self.mqtt_message_edit.text(),
            'mqttTopic': self.mqtt_topic_edit.text(),
            'soundEnabled': self.sound_enabled_checkbox.isChecked(),
            'sound': self.sound_edit.text(),
            'keyEnabled': self.key_enabled_checkbox.isChecked(),
            'pageEnabled': self.page_enabled_checkbox.isChecked(),
            'page': self.page_combo.currentData()
        }
        clipboard = QApplication.clipboard()
        clipboard.setText(json.dumps(settings))

    def paste_settings(self):
        clipboard = QApplication.clipboard()
        settings = clipboard.text()
        try:
            settings = json.loads(settings)
            if ('dataType' not in settings):
                return
            self.key_edit.setText(settings['key'])
            self.red_combo.setCurrentIndex(settings['r'])
            self.green_combo.setCurrentIndex(settings['g'])
            self.mqtt_enabled_checkbox.setChecked(settings['mqttEnabled'])
            self.mqtt_message_edit.setText(settings['mqttMessage'])
            self.mqtt_topic_edit.setText(settings['mqttTopic'])
            self.sound_enabled_checkbox.setChecked(settings['soundEnabled'])
            self.sound_edit.setText(settings['sound'])
            self.key_enabled_checkbox.setChecked(settings['keyEnabled'])
            self.page_enabled_checkbox.setChecked(settings['pageEnabled'])
            self.page_combo.setCurrentIndex(settings['page'] - 1)
        except (json.JSONDecodeError, KeyError):
            QMessageBox.warning(self, "Error", "Invalid clipboard data")
            
        self.toggle_mqtt_fields()
        self.toggle_sound_fields()
        self.toggle_key_field()
        self.toggle_page_field()

    def toggle_mqtt_fields(self):
        is_checked = self.mqtt_enabled_checkbox.isChecked()
        self.mqtt_message_edit.setEnabled(is_checked)
        self.mqtt_topic_edit.setEnabled(is_checked)

    def toggle_sound_fields(self):
        is_checked = self.sound_enabled_checkbox.isChecked()
        self.sound_edit.setEnabled(is_checked)

    def toggle_key_field(self):
        is_checked = self.key_enabled_checkbox.isChecked()
        self.key_edit.setEnabled(is_checked)

    def toggle_page_field(self):
        is_checked = self.page_enabled_checkbox.isChecked()
        self.page_combo.setEnabled(is_checked)

