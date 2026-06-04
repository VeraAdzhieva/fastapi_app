from pathlib import Path

import numpy as np
import onnxruntime as onnx

CURRENT_DIR = Path(__file__).resolve().parent

MODEL_PATH = CURRENT_DIR / "diabetes_model.onnx"


class OnnxPredict:
    """
    Сервис ONNX.
    """

    def __init__(self) -> None:
        """
        Инициализация.
        """
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Модель {MODEL_PATH} не найдена \n")

        self.session = onnx.InferenceSession(str(MODEL_PATH))
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, features: np.ndarray) -> float:
        """
        Обращение к модели.
        """
        result = self.session.run(None, {self.input_name: features})
        return float(result[0][0])
