from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Predict:
    """
    Запрос расчета вероятности диабета.
    """
    pregnancies: int
    glucose: int
    bmi: float
    age: int

    def to_features_array(self) -> np.ndarray:
        features = [self.pregnancies, self.glucose, self.bmi, self.age]
        return np.array([features], dtype=np.float32)
    

@dataclass(frozen=True)
class Register:
    """
    Запрос на регистрацию.
    """
    username: str
    password: str
    firstname: str
    lastname: str

@dataclass(frozen=True)
class LoginIn:
    """
    Авторизация.
    """
    username: str
    password: str