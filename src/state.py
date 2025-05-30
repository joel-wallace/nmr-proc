from dataclasses import dataclass, field
from typing import List, Optional
from PySide6.QtCore import QObject, Signal

@dataclass
class Experiment:
    number: int
    nucleus: Optional[str]  # "1H", "19F", or None
    path: str

class AppState(QObject):
    experiments_changed = Signal()

    def __init__(self):
        super().__init__()
        self.selected_directory: Optional[str] = None
        self.experiments: List[Experiment] = []

    def add_experiment(self, experiment):
        self.experiments.append(experiment)
        self.experiments_changed.emit()

    def get_experiment_by_number(self, number: int) -> Optional[Experiment]:
        return next((exp for exp in self.experiments if exp.number == number), None)

    def get_experiment_numbers_by_nucleus(self, nucleus: str) -> List[int]:
        return [exp.number for exp in self.experiments if exp.nucleus == nucleus]
