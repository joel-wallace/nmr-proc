# main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTreeView, QSplitter,
    QFileDialog, QPushButton, QFileSystemModel, QLabel,
    QMenuBar, QMenu, QSlider, QHBoxLayout, QLineEdit
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QDir
import pyqtgraph as pg
import numpy as np

from .utils import shorten_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR PROCESSING :)")
        self.resize(1000, 600)

        self.ppm = None
        self.data = None
        self.current_offset = 0.0

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        splitter = QSplitter(Qt.Horizontal)
        left_splitter = QSplitter(Qt.Vertical)

        # Left upper panel
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

        left_upper_panel = QWidget()
        left_upper_layout = QVBoxLayout()
        left_upper_layout.addWidget(self.open_button)
        left_upper_layout.addWidget(self.path_label)
        left_upper_layout.addWidget(self.tree)
        left_upper_panel.setLayout(left_upper_layout)

        # Left lower panel
        left_lower_panel = QWidget()
        left_lower_layout = QVBoxLayout()

        def add_labeled_lineedit(layout, label_text):
            lbl = QLabel(label_text)
            le = QLineEdit()
            le.setMaximumWidth(100)
            layout.addWidget(lbl)
            layout.addWidget(le)
            return le

        self.h_experiment_edit = add_labeled_lineedit(left_lower_layout, "H Exp")

        self.process_1h_button = QPushButton("Process 1H")
        self.process_1h_button.clicked.connect(self.handle_process_1h)
        left_lower_layout.addWidget(self.process_1h_button)

        self.p0_slider = QSlider(Qt.Horizontal)
        self.p0_slider.setRange(-90, 90)
        self.p0_slider.setValue(0)
        self.p0_slider.valueChanged.connect(self.update_spectrum_from_slider)
        self.p0_label = QLabel("p0: 0")
        left_lower_layout.addWidget(self.p0_label)
        left_lower_layout.addWidget(self.p0_slider)

        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(-300, 300)
        self.offset_slider.setValue(0)
        self.offset_slider.valueChanged.connect(self.update_offset)
        self.offset_slider.sliderPressed.connect(self.update_offset)
        self.offset_slider.sliderReleased.connect(self.finish_offset)
        self.offset_label = QLabel("Offset: 0.00 ppm")
        left_lower_layout.addWidget(self.offset_label)
        left_lower_layout.addWidget(self.offset_slider)

        left_lower_panel.setLayout(left_lower_layout)

        # Right panel
        self.plot_widget = pg.PlotWidget()
        self.green_line = pg.InfiniteLine(pos=100.0, angle=90, pen=pg.mkPen('g', width=2))
        self.plot_widget.addItem(self.green_line)

        menubar = QMenuBar()

        view_menu = QMenu("View", self)
        reset_view_action = QAction("Reset View", self)
        view_menu.addAction(reset_view_action)

        analysis_menu = QMenu("Analysis", self)
        fit_peaks_action = QAction("Fit Peaks", self)
        integrate_action = QAction("Peak Integral", self)
        bootstrap_action = QAction("Bootstrapping", self)
        analysis_menu.addActions([fit_peaks_action, integrate_action, bootstrap_action])

        export_menu = QMenu("Export", self)
        export_image_action = QAction("Image", self)
        export_menu.addAction(export_image_action)

        menubar.addMenu(view_menu)
        menubar.addMenu(analysis_menu)
        menubar.addMenu(export_menu)

        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)
        right_layout.addWidget(menubar)
        right_layout.addWidget(self.plot_widget)
        right_panel.setLayout(right_layout)

        self.plot_placeholder_data()

        left_splitter.addWidget(left_upper_panel)
        left_splitter.addWidget(left_lower_panel)

        splitter.addWidget(left_splitter)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.model.setRootPath(directory)
            self.tree.setRootIndex(self.model.index(directory))
            self.path_label.setText(shorten_path(directory))

    def plot_placeholder_data(self):
        x = np.linspace(-200, 200, 1000)
        y = np.exp(-0.01 * x ** 2) * np.cos(0.2 * x)
        self.plot_widget.plot(x, y, pen='b')
        self.plot_widget.setLabel('left', 'Intensity')
        self.plot_widget.setLabel('bottom', 'Chemical Shift (ppm)')
        self.plot_widget.setTitle("Placeholder Spectrum")
        self.plot_widget.getPlotItem().invertX(True)

    def handle_process_1h(self):
        from processing.file import process_1h_spectrum

        directory = self.model.filePath(self.tree.rootIndex())
        h_exp = self.h_experiment_edit.text().strip()
        if not h_exp.isdigit():
            print("Invalid experiment number")
            return

        try:
            p0 = self.p0_slider.value()
            offset = self.offset_slider.value() / 1000.0
        except ValueError:
            print("Invalid numeric input.")
            return

        try:
            ppm, data = process_1h_spectrum(directory, h_exp, p0=p0, offset=offset)
        except Exception as e:
            print("Processing failed:", e)
            return

        self.ppm = ppm
        self.data = data
        self.current_offset = offset

        self.update_plot(ppm, data)

    def update_spectrum_from_slider(self):
        self.p0_label.setText(f"p0: {self.p0_slider.value()}")
        self.handle_process_1h()

    def update_offset(self):
        self.offset_label.setText(f"Offset: {self.offset_slider.value()/1000.0:.3f} ppm")
        self.handle_process_1h()
        self.plot_widget.setXRange(-0.5, 0.5)
        self.green_line.setPos(0.0)

    def finish_offset(self):
        self.plot_widget.setXRange(-1, 12)
        self.green_line.setPos(100)

    def update_plot(self, ppm, data):
        self.plot_widget.clear()
        self.plot_widget.plot(ppm, data, pen='b')
        self.plot_widget.setLabel('left', 'Intensity')
        self.plot_widget.setLabel('bottom', 'Chemical Shift (ppm)')
        self.plot_widget.setTitle("1H NMR Spectrum")
        self.plot_widget.getPlotItem().invertX(True)
        self.plot_widget.addItem(self.green_line)

        y_min, y_max = min(data), max(data)
        zoom_factor = 5
        self.plot_widget.setYRange(y_min / zoom_factor, y_max / zoom_factor)
        self.plot_widget.setXRange(-1, 12)