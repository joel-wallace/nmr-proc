from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel,
    QVBoxLayout, QComboBox, QPushButton, 
    QFileDialog
        )

from PySide6.QtCore import Qt

# 1D 1H Experiment number (read acqus file from each directory and list 1H experiments in a dropdown)

class ProtonPanel(QWidget):
    def __init__(self, app_state):
        super().__init__()
        self.app_state = app_state
        self.layout = QVBoxLayout()

        exp_layout = QHBoxLayout()
        exp_layout.addWidget(QLabel("1D 1H:", alignment=Qt.AlignRight))

        self.exp_dropdown = QComboBox()
        exp_layout.addWidget(self.exp_dropdown)

        self.exp_plot_button = QPushButton("Plot")
        # TODO: Plot should set the spectrum in the state, which in turn should trigger plotting
        exp_layout.addWidget(self.exp_plot_button)

        self.layout.addLayout(exp_layout)
        self.setLayout(self.layout)

        self.app_state.experiments_changed.connect(self.populate_dropdown)

        self.populate_dropdown()

    def populate_dropdown(self):
        self.exp_dropdown.clear()
        one_h_numbers = self.app_state.get_experiment_numbers_by_nucleus("1H")
        for num in sorted(one_h_numbers):
            self.exp_dropdown.addItem(str(num))
