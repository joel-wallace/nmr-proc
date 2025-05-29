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

        h_experiment_layout = QHBoxLayout()
        h_experiment_label = QLabel("1H Exp:")
        self.h_experiment_edit = QLineEdit()
        h_experiment_layout.addWidget(h_experiment_label)
        h_experiment_layout.addWidget(self.h_experiment_edit)
        self.process_1h_button = QPushButton("Process")
        self.process_1h_button.clicked.connect(self.handle_process_1h)
        h_experiment_layout.addWidget(self.process_1h_button)

        left_lower_layout.addLayout(h_experiment_layout)

        self.p0_slider = QSlider(Qt.Horizontal)
        self.p0_slider.setRange(-90, 90)
        self.p0_slider.setValue(0)
        self.p0_slider.valueChanged.connect(self.update_spectrum_from_slider)
        self.p0_label = QLabel("p0: 0")
        self.baseline_1h_button = QPushButton("Baseline")
        self.baseline_1h_button.clicked.connect(self.baseline_1h)
        p0_layout = QHBoxLayout()
        p0_layout.addWidget(self.p0_label)
        p0_layout.addWidget(self.p0_slider)
        p0_layout.addWidget(self.baseline_1h_button)
        left_lower_layout.addLayout(p0_layout)

        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(-300, 300)
        self.offset_slider.setValue(0)
        self.offset_slider.valueChanged.connect(self.update_offset)
        self.offset_slider.sliderPressed.connect(self.update_offset)
        self.offset_slider.sliderReleased.connect(self.finish_offset)
        self.offset_label = QLabel("Offset:\n0.00 ppm")
        offset_layout = QHBoxLayout()
        offset_layout.addWidget(self.offset_label)
        offset_layout.addWidget(self.offset_slider)
        self.save_offset_button = QPushButton("Save")
        self.save_offset_button.clicked.connect(self.save_offset)
        offset_layout.addWidget(self.save_offset_button)
        left_lower_layout.addLayout(offset_layout)

        self.h_offset = 0
        self.f_offset = 0

        left_lower_panel.setLayout(left_lower_layout)

        # Right panel
        self.plot_widget = pg.PlotWidget()
        self.green_line = pg.InfiniteLine(pos=1000.0, angle=90, pen=pg.mkPen('g', width=2))
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

    def save_offset(self):
        self.h_offset = self.offset_slider.value() / 1000.0
        self.f_offset = self.h_offset * 0.94

    def plot_placeholder_data(self):
        import numpy as np
        import pyqtgraph as pg

        x = np.linspace(0, 4 * np.pi, 1000)
        y = np.sin(x)

        self.plot_widget.clear()
        self.plot_widget.plot(x, y, pen=pg.mkPen('orange', width=2))
        self.plot_widget.setLabel('left', 'Amplitude')
        self.plot_widget.setLabel('bottom', 'Time')
        self.plot_widget.setTitle("Sine Wave")
        self.plot_widget.getPlotItem().invertX(False)



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

    def baseline_1h(self):
        from processing.file import baseline_1h_spectrum
        self.data = baseline_1h_spectrum(self.data)
        self.update_plot(self.ppm, self.data)

    def update_spectrum_from_slider(self):
        self.p0_label.setText(f"p0: {self.p0_slider.value()}")
        self.handle_process_1h()

    def update_offset(self):
        self.offset_label.setText(f"Offset:\n{self.offset_slider.value()/1000.0:.3f} ppm")
        self.handle_process_1h()
        self.plot_widget.setXRange(-0.5, 0.5)
        self.green_line.setPos(0.0)

    def finish_offset(self):
        self.plot_widget.setXRange(-1, 12)
        self.green_line.setPos(1000)
        self.baseline_1h()

    def update_plot(self, ppm, data):
        self.plot_widget.clear()
        self.plot_widget.plot(ppm, data, pen='w')
        self.plot_widget.setLabel('left', 'Intensity')
        self.plot_widget.setLabel('bottom', 'Chemical Shift (ppm)')
        self.plot_widget.setTitle("1H NMR Spectrum")
        self.plot_widget.getPlotItem().invertX(True)
        self.plot_widget.addItem(self.green_line)

        y_min, y_max = min(data), max(data)
        zoom_factor = 5
        self.plot_widget.setYRange(y_min / zoom_factor, y_max / zoom_factor)
        self.plot_widget.setXRange(-1, 12)
