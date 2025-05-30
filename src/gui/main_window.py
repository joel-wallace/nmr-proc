from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter,
    QVBoxLayout,
        )
from PySide6.QtCore import Qt, QDir

import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR-Proc 0.2.0")
        self.resize(1000, 600)
        self.init_main_ui()
        # State should go somewhere in here
    
    def init_main_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.setCentralWidget(main_widget)
        main_splitter = QSplitter(Qt.Horizontal)
        left_main_panel = QSplitter(Qt.Vertical)
        self.plot_widget = pg.PlotWidget()

        # Create file_tree and add to left_main_panel
        # Create tab panel and add to left_main_panel
        left_main_panel.setSizes([40,60])

        main_splitter.addWidget(left_main_panel)
        main_splitter.addWidget(self.plot_widget)
        main_splitter.setSizes([30,70])
        main_layout.addWidget(main_splitter)
        main_widget.setLayout(main_layout)
