# main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTreeView, QSplitter,
    QFileDialog, QPushButton, QFileSystemModel, QLabel,
    QMenuBar, QMenu, QSlider, QHBoxLayout, QLineEdit,
    QTabWidget
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
        left_lower_panel = QTabWidget()
        h_tab_layout = QVBoxLayout()
        f_tab_layout = QVBoxLayout()

        h_experiment_layout = QHBoxLayout()
        h_experiment_label = QLabel("1H Exp:")
        self.h_experiment_edit = QLineEdit()
        h_experiment_layout.addWidget(h_experiment_label)
        h_experiment_layout.addWidget(self.h_experiment_edit)
        self.process_1h_button = QPushButton("Plot")
        self.process_1h_button.clicked.connect(self.handle_process_1h)
        h_experiment_layout.addWidget(self.process_1h_button)

        h_tab_layout.addLayout(h_experiment_layout)

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
        h_tab_layout.addLayout(p0_layout)

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
        h_tab_layout.addLayout(offset_layout)

        self.h_offset = 0
        self.f_offset = 0

        f_experiment_layout = QHBoxLayout()
        f_experiment_label = QLabel("19F exps:")
        self.f_experiment_1_edit = QLineEdit()
        f_experiment_to_label = QLabel("to")
        self.f_experiment_2_edit = QLineEdit()
        self.process_19f_button = QPushButton("Plot")
        self.process_19f_button.clicked.connect(self.handle_process_19f)
        f_experiment_layout.addWidget(f_experiment_label)
        f_experiment_layout.addWidget(self.f_experiment_1_edit)
        f_experiment_layout.addWidget(f_experiment_to_label)
        f_experiment_layout.addWidget(self.f_experiment_2_edit)
        f_experiment_layout.addWidget(self.process_19f_button)
        f_tab_layout.addLayout(f_experiment_layout)

        self.baseline_19f_button = QPushButton("Baseline")
        self.baseline_19f_button.clicked.connect(self.baseline_19f)
        # num_peaks_label = QLabel("Num. peaks")
        self.fit_peaks_button = QPushButton("Fit")
        self.fit_peaks_button.clicked.connect(self.fit_peaks_19f)
        basic_19f_layout = QHBoxLayout()
        basic_19f_layout.addWidget(self.baseline_19f_button)
        # basic_19f_layout.addWidget(num_peaks_label)
        # basic_19f_layout.addWidget(self.num_peaks_edit)
        basic_19f_layout.addWidget(self.fit_peaks_button)
        f_tab_layout.addLayout(basic_19f_layout)

        f_tab_layout.addWidget(QLabel("Peak initial guesses:"))

        self.peak_guess_edits = [QLineEdit("-61.7"),QLineEdit("0"),QLineEdit("0"),QLineEdit("0")]

        peak_1_guess_label = QLabel("N:")
        peak_1_guess_layout = QHBoxLayout()
        peak_1_guess_layout.addWidget(peak_1_guess_label)
        peak_1_guess_layout.addWidget(self.peak_guess_edits[0])

        peak_2_guess_label = QLabel("U:")
        peak_2_guess_layout = QHBoxLayout()
        peak_2_guess_layout.addWidget(peak_2_guess_label)
        peak_2_guess_layout.addWidget(self.peak_guess_edits[1])

        peak_3_guess_label = QLabel("I1:")
        peak_3_guess_layout = QHBoxLayout()
        peak_3_guess_layout.addWidget(peak_3_guess_label)
        peak_3_guess_layout.addWidget(self.peak_guess_edits[2])

        peak_4_guess_label = QLabel("I2:")
        peak_4_guess_layout = QHBoxLayout()
        peak_4_guess_layout.addWidget(peak_4_guess_label)
        peak_4_guess_layout.addWidget(self.peak_guess_edits[3])

        peak_guess_layout = QHBoxLayout()
        peak_guess_layout.addLayout(peak_1_guess_layout)
        peak_guess_layout.addLayout(peak_2_guess_layout)
        peak_guess_layout.addLayout(peak_3_guess_layout)
        peak_guess_layout.addLayout(peak_4_guess_layout)
        f_tab_layout.addLayout(peak_guess_layout)

        h_proc_tab = QWidget()
        h_proc_tab.setLayout(h_tab_layout)

        f_proc_tab = QWidget()
        f_proc_tab.setLayout(f_tab_layout)

        left_lower_panel.addTab(h_proc_tab, "1H")
        left_lower_panel.addTab(f_proc_tab, "19F")

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

        self.update_plot(ppm, data, "1H")

    def handle_process_19f(self):
        from processing.file import process_sum_19f_spectra

        directory = self.model.filePath(self.tree.rootIndex())
        exp1 = self.f_experiment_1_edit.text().strip()
        exp2 = self.f_experiment_2_edit.text().strip()
        if not (exp1.isdigit() and exp2.isdigit()):
            print("Invalid experiment number")
            return
        offset = self.f_offset

        try:
            ppm, data = process_sum_19f_spectra(directory, exp1, exp2, offset)
        except Exception as e:
            print("Processing failed:", e)
            return
        
        self.ppm = ppm
        self.data = data
        self.update_plot(ppm,data,"19F")

    def baseline_1h(self):
        from processing.file import baseline_1h_spectrum
        self.data = baseline_1h_spectrum(self.data)
        self.update_plot(self.ppm, self.data,"1H")

    def baseline_19f(self):
        from processing.file import baseline_19f_spectrum
        self.ppm, self.data = baseline_19f_spectrum(self.ppm, self.data)
        self.update_plot(self.ppm, self.data,"19F")

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
    
    def fit_peaks_19f(self):
        self.update_plot(self.ppm, self.data, "19F")
        from processing.file import fit_lorentzian_curves
        # num_peaks = int(self.num_peaks_edit.text().strip())
        peak_guesses = []
        for guess in self.peak_guess_edits:
            value = float(guess.text().strip())
            if value != 0:
                peak_guesses.append(value)
        curves = fit_lorentzian_curves(self.ppm,self.data,peak_guesses)
        colours = ["blue", "orange", "green", "yellow", "red"]
        for i, curve in enumerate(curves):
            fit_ppm, fit_data = curve
            self.plot_widget.plot(fit_ppm, fit_data, pen=pg.mkPen(colours[i], width=2.5))

    def update_plot(self, ppm, data, nucleus):
        self.plot_widget.clear()
        self.plot_widget.plot(ppm, data, pen='w')
        self.plot_widget.setLabel('left', 'Intensity')
        self.plot_widget.setLabel('bottom', 'Chemical Shift (ppm)')
        y_min, y_max = min(data), max(data)
        if nucleus == "1H":
            self.plot_widget.setTitle("1H NMR Spectrum")
            self.plot_widget.addItem(self.green_line)
            self.plot_widget.setXRange(-1, 12)
            zoom_factor = 5
            self.plot_widget.setYRange(y_min / zoom_factor, y_max / zoom_factor)
        elif nucleus == "19F":
            self.plot_widget.setTitle("19F NMR Spectrum")
            self.plot_widget.setXRange(-58, -65)
            zoom_factor = 5
            self.plot_widget.setYRange(y_min, y_max)
        self.plot_widget.getPlotItem().invertX(True)
        
        
        
        
