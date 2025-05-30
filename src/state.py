from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Experiment:
    number: int
    nucleus: Optional[str]  # "1H", "19F", or None
    path: str


@dataclass
class AppState:
    selected_directory: Optional[str] = None
    experiments: List[Experiment] = field(default_factory=list)

    def get_experiment_by_number(self, number: int) -> Optional[Experiment]:
        return next((exp for exp in self.experiments if exp.number == number), None)
