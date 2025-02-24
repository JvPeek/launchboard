import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QDockWidget, QToolBar, QAction, QMessageBox, QStyleFactory, QDialog, QPushButton, QLabel, QVBoxLayout
)
import hashlib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap
from button_settings_widget import ButtonSettingsWidget
from grid_widget import GridWidget
from settings_widget import SettingsWidget
from constants import CONFIG_FILE, PAGES





class MainWindow(QMainWindow):
    docHash = ""
    def __init__(self):
        super().__init__()
        
        app.setStyleSheet(open('./style/Combinear.qss').read() + open('./style/style.css').read())
        

        self.tab_widget = QTabWidget()
        self.setWindowTitle("LaunchBoard")
        self.setWindowIcon(QIcon('logo.png'))

        self.grids = []
        for i in range(PAGES):
            grid_widget = GridWidget(self)

            self.tab_widget.addTab(grid_widget, f"PAGE{i+1}")
            self.grids.append(grid_widget)

        

        settings_widget = SettingsWidget(self)
        self.tab_widget.addTab(settings_widget, f"Settings")
        
        self.setCentralWidget(self.tab_widget)

        self.dock_widget = QDockWidget("Button Settings", self)
        self.dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dock_widget.setVisible(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        self.load_config()

        # Add toolbar for copy/paste entire page
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        load_action = QAction("Reload Config", self)
        load_action.setShortcut(QKeySequence("Ctrl+L"))
        load_action.triggered.connect(self.load_config)
        self.toolbar.addAction(load_action)
        
        save_action = QAction("Save Config", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_config)
        self.toolbar.addAction(save_action)

        copy_page_action = QAction("Copy Page", self)
        copy_page_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        copy_page_action.triggered.connect(self.copy_page)
        self.toolbar.addAction(copy_page_action)

        paste_page_action = QAction("Paste Page", self)
        paste_page_action.setShortcut(QKeySequence("Ctrl+Shift+V"))
        paste_page_action.triggered.connect(self.paste_page)
        self.toolbar.addAction(paste_page_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        self.toolbar.addAction(about_action)
    def toggleStyle():
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.LightPalette) + open('./style.css').read())
        

    def show_about_dialog(self):
        dlg = QDialog()

        layout = QVBoxLayout()

        b1 = QPushButton("ok")
        b1.clicked.connect(dlg.close)
        
        self.logo = QLabel(self)

        pixmap = QPixmap('./icon.png')

        self.logo.resize(256, 256)
        self.logo.setPixmap(pixmap.scaled(self.logo.size()))
        self.text = QLabel(self)
        self.text.setText("Made by JvPeek\n\nThis is still a work in progress.")
        
        

        layout.addWidget(self.logo)


        layout.addWidget(self.text)
        layout.addStretch()
        layout.addWidget(b1)
        self.show()  
        dlg.setLayout(layout)
        dlg.setWindowTitle("About") 
        # dlg.resize(250,300)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
    
    def open_settings(self, button):
        settings_widget = ButtonSettingsWidget(button, self)
        self.dock_widget.setWidget(settings_widget)
        self.dock_widget.setVisible(True)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.save_config()  # Create the default config file if it doesn't exist

        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)

        for i, grid in enumerate(self.grids):
            if f"tab_{i + 1}" in config:
                grid.load_from_config(config[f"tab_{i + 1}"])
        self.docHash = self.getHashData()


    def save_config(self):
        
        self.docHash = self.getHashData()
        config = {}
        for i, grid in enumerate(self.grids):
            config[f"tab_{i + 1}"] = grid.get_config()
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)

    def closeEvent(self, event):
        if not (self.docHash == self.getHashData()):
            reply = QMessageBox.question(self, 'Save Configuration',
                                         "Do you want to save the current configuration before exiting?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                self.save_config()

        event.accept()
    def getHashData(self):
        data = ""
        for grid in self.grids:
            thisHash = json.dumps(grid.get_config())
            
            data = data + thisHash
        data = hashlib.md5(data.encode('utf-8')).hexdigest()
        return data
    def copy_page(self):
        
        self.getHashData()
        current_index = self.tab_widget.currentIndex()
        if (current_index >= PAGES):
            return
        current_grid = self.grids[current_index]
        page_config = current_grid.get_config()
        clipboard = QApplication.clipboard()
        print((json.dumps(page_config)))
        clipboard.setText(json.dumps(page_config))

    def paste_page(self):
        current_index = self.tab_widget.currentIndex()
        if (current_index >= PAGES):
            return
        current_grid = self.grids[current_index]
        clipboard = QApplication.clipboard()
        page_config = clipboard.text()
        try:
            page_config = json.loads(page_config)
            current_grid.set_config(page_config)
        except (json.JSONDecodeError, KeyError):
            QMessageBox.warning(self, "Error", "Invalid clipboard data")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
