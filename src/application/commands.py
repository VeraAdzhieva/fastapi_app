from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Predict:
    pregnancies: int
    glucose: int
    bmi: float
    age: int

    def to_features_array(self) -> np.ndarray:
        features = [self.pregnancies, self.glucose, self.bmi, self.age]
        return np.array([features], dtype=np.float32)
