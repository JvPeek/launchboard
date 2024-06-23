import json
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt


from constants import COLOR_VALUES

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        
        layout = QGridLayout()
        layout.setProperty("class", "gridLayout")

        layout.setSpacing(8)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)
