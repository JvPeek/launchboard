import json
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt


from constants import COLOR_VALUES, PAGES

class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        
        layout = QGridLayout()
        layout.setProperty("class", "gridLayout")

        layout.setSpacing(8)
        layout.setContentsMargins(0,0,0,0)

        self.buttons = []
        for i in range(9):
            row_buttons = []
            for j in range(9):
                button = QPushButton('None')
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setFocusPolicy(Qt.NoFocus)
                if (i!=0 or j != 8):
                    button.clicked.connect(self.button_clicked)
                else:
                    button.hide()
                if (i==0) or (j==8):
                    button.setProperty("class", "roundButton")
                    
                else:
                    button.setProperty("class", "gridButton")
                    
                
                layout.addWidget(button, i, j)
                    
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.setLayout(layout)

    def button_clicked(self):
        button = self.sender()
        self.parent_window.open_settings(button)

    def load_from_config(self, config):
        for i in range(9):
            for j in range(9):
                btn_config = config[i * 9 + j]
                button = self.buttons[i][j]
                button.setText(btn_config.get('key', 'None'))
                red_value = COLOR_VALUES[btn_config.get('r', 0)]
                green_value = COLOR_VALUES[btn_config.get('g', 0)]
                color_code = f"#{red_value}{green_value}00"
                button.setStyleSheet(f"background-color: {color_code};")

    def get_config(self):
        config = [
            {
                'key': button.text(),
                'r': list(COLOR_VALUES.values()).index(button.styleSheet().split(': ')[-1][1:3]) if button.styleSheet() else 0,
                'g': list(COLOR_VALUES.values()).index(button.styleSheet().split(': ')[-1][3:5]) if button.styleSheet() else 0,
            }
            for row in self.buttons for button in row
        ]
        return config

    def set_config(self, config):
        self.load_from_config(config)
