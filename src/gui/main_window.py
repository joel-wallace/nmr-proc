from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter,
    QVBoxLayout, QTabWidget
        )
from PySide6.QtCore import Qt, QDir

import pyqtgraph as pg

from gui.file_panel import FilePanel
from gui.proton_panel import ProtonPanel
from state import AppState

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR-Proc 0.2.0")
        self.resize(1000, 600)

        self.app_state = AppState()

        self.init_main_ui()
    
    def init_main_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.setCentralWidget(main_widget)
        main_splitter = QSplitter(Qt.Horizontal)
        left_main_panel = QSplitter(Qt.Vertical)
        self.plot_widget = pg.PlotWidget(background="w")

        # Create file_tree and add to left_main_panel
        self.file_panel = FilePanel(self.app_state)
        left_main_panel.addWidget(self.file_panel)

        control_panel = QTabWidget()
        self.proton_panel = ProtonPanel(self.app_state)
        control_panel.addTab(self.proton_panel, "1H")
        left_main_panel.addWidget(control_panel)
        # Create tab panel and add to left_main_panel
        left_main_panel.setSizes([5000,5000])

        main_splitter.addWidget(left_main_panel)
        main_splitter.addWidget(self.plot_widget)
        main_splitter.setSizes([3000,7000])
        main_layout.addWidget(main_splitter)
        main_widget.setLayout(main_layout)
