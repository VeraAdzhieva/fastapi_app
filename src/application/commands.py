from dataclasses import dataclass

@dataclass(frozen=True)
class Predict:
    Pregnancies: int
    Glucose: int
    BMI: float
    Age: int

    def to_features_array(self) -> list:
        return [self.Pregnancies, self.Glucose, self.BMI, self.Age] 