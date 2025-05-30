from PySide6.QtWidgets import (
    QWidget, QListWidgetItem, QListWidget,
    QVBoxLayout, QPushButton, QLineEdit, 
    QFileDialog,
        )

from PySide6.QtGui import QFont, QColor, QBrush

from PySide6.QtCore import QDir

import os
import re

from input.bruker import map_nmr_directory
from state import Experiment

class FilePanel(QWidget):
    def __init__(self, app_state):
        super().__init__()
        self.app_state = app_state

        self.open_button = QPushButton("Select Directory")
        self.open_button.clicked.connect(self.select_directory)

        self.path_edit = QLineEdit("No directory selected")
        self.path_edit.setReadOnly(True)

        self.list_widget = QListWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.path_edit)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def get_dir_path(self):
        return self.path_edit.text()

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.path_edit.setText(directory)
            self.app_state.selected_directory = directory

            self.app_state.experiments.clear()
            entries = map_nmr_directory(directory)

            for entry in entries:
                self.app_state.experiments.append(Experiment(
                    number=int(entry["name"]),
                    nucleus=entry["type"],
                    path=os.path.join(directory, entry["name"])
                ))

            self.populate_experiment_list()

    def populate_experiment_list(self):
        self.list_widget.clear()
        font = QFont("Inter", 10)
    
        for exp in sorted(self.app_state.experiments, key=lambda e: e.number):
            nucleus = exp.nucleus or "Unprocessed"
            item = QListWidgetItem(f"{exp.number:<4} ({nucleus})")
            item.setFont(font)
    
            color = {
                "1H": "#0059FF",
                "19F": "#01d436",
                None: "#FF0000"
            }.get(exp.nucleus, "#FF0000")
    
            item.setForeground(QBrush(QColor(color)))
            self.list_widget.addItem(item)
