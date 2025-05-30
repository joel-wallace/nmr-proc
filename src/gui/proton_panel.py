from PySide6.QtWidgets import (
    QWidget, QTreeView, QFileSystemModel,
    QVBoxLayout, QPushButton, QLineEdit, 
    QFileDialog
        )

# 1D 1H Experiment number (read acqus file from each directory and list 1H experiments in a dropdown)

class ProtonPanel(QWidget):
    def __init__(self):
        super().__init__()