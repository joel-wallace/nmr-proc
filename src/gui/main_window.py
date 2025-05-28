from PySide6.QtWidgets import QMainWindow
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.plot_nmr_data()

    def plot_nmr_data(self):
        # Example: simulated NMR-like data
        x = np.linspace(0, 10, 1000)
        y = np.exp(-x) * np.cos(20 * x)
        self.plot_widget.plot(x, y, pen='c')

