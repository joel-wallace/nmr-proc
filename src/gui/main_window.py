from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter,
    QVBoxLayout,
        )
from PySide6.QtCore import Qt, QDir

import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR-Proc")
        self.resize(1000, 600)

        # State should go somewhere in here
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.setCentralWidget(main_widget)
        main_splitter = QSplitter(Qt.Horizontal)
        left_main_panel = QSplitter(Qt.Vertical)
        self.plot_widget = pg.PlotWidget()

        main_splitter.addWidget(left_main_panel)
        main_splitter.addWidget(self.plot_widget)
        main_layout.addWidget(main_splitter)
        main_widget.setLayout(main_layout)
