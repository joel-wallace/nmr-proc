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

class FilePanel(QWidget):
    def __init__(self):
        super().__init__()

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
            self.populate_experiment_list(directory)

    def populate_experiment_list(self, directory):
        self.list_widget.clear()

        font = QFont("Inter", 10)

        entries = sorted(
            map_nmr_directory(directory),
            key=lambda entry: int(entry["name"])
        )

        for entry in entries:
            name = entry["name"]
            exp_type = entry["type"] or "Unprocessed"

            item = QListWidgetItem(f"{name:<4} ({exp_type})")
            item.setFont(font)

            # Optional: color-code by type
            if exp_type == "1H":
                item.setForeground(QBrush(QColor("#0059FF")))  # Blue
            elif exp_type == "19F":
                item.setForeground(QBrush(QColor("#01d436")))  # Green
            else:
                item.setForeground(QBrush(QColor("#FF0000")))  # Red

            self.list_widget.addItem(item)
