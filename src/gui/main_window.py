from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QTreeView, QSplitter, QFileDialog,
    QPushButton, QFileSystemModel, QLabel,
    QMenuBar, QMenu
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QDir
import pyqtgraph as pg
import numpy as np
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR Processor")
        self.resize(1000, 600)

        # Central layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        splitter = QSplitter(Qt.Horizontal)

        # Left panel setup
        self.open_button = QPushButton("Open Directory")
        self.open_button.clicked.connect(self.select_directory)

        self.path_label = QLabel("No directory selected")
        self.path_label.setWordWrap(True)

        self.tree = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.open_button)
        left_layout.addWidget(self.path_label)
        left_layout.addWidget(self.tree)
        left_panel.setLayout(left_layout)

        # Right panel
        self.plot_widget = pg.PlotWidget()
        # Create menubar
        menubar = QMenuBar()
        # menubar.setMovable(False)

        # View Menu
        view_menu = QMenu("View", self)
        reset_view_action = QAction("Reset View", self)
        view_menu.addAction(reset_view_action)

        # Analysis Menu
        analysis_menu = QMenu("Analysis", self)
        fit_peaks_action = QAction("Fit Peaks", self)
        integrate_action = QAction("Peak Integral", self)
        bootstrap_action = QAction("Bootstrapping", self)
        analysis_menu.addActions([fit_peaks_action, integrate_action, bootstrap_action])

        # Export Menu
        export_menu = QMenu("Export", self)
        export_image_action = QAction("Image", self)
        export_menu.addAction(export_image_action)

        # Add menus as tool buttons
        menubar.addMenu(view_menu)
        menubar.addMenu(analysis_menu)
        menubar.addMenu(export_menu)

        # Right panel container: menubar + plot
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)
        right_layout.addWidget(menubar)
        right_layout.addWidget(self.plot_widget)
        right_panel.setLayout(right_layout)

        # Replace this:
        # splitter.addWidget(self.plot_widget)
        # With this:
        

        self.plot_placeholder_data()

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        # splitter.addWidget(self.plot_widget)
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.model.setRootPath(directory)
            self.tree.setRootIndex(self.model.index(directory))
            self.path_label.setText(self.shorten_path(directory))

    def shorten_path(self, path, max_length=50):
        if len(path) <= max_length:
            return path
        parts = path.split(os.sep)
        for i in range(len(parts)):
            shortened = os.sep.join(["..."] + parts[i:])
            if len(shortened) <= max_length:
                return shortened
        return "..." + path[-(max_length - 3):]  # fallback

    def plot_placeholder_data(self):
        x = np.linspace(-200, 200, 1000)
        y = np.exp(-0.01 * x ** 2) * np.cos(0.2 * x)
        self.plot_widget.plot(x, y, pen='b')
        self.plot_widget.setLabel('left', 'Intensity')
        self.plot_widget.setLabel('bottom', 'Chemical Shift (ppm)')
        self.plot_widget.setTitle("Placeholder Spectrum")
        self.plot_widget.getPlotItem().invertX(True)

# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

