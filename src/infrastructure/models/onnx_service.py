import onnxruntime as ort
import numpy as np
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

MODEL_PATH = CURRENT_DIR / "diabetes_model.onnx"

class OnnxPredict:
    """
    Сервис ONNX.
    """
    def __init__(self):
        """
        Инициализация.
        """
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Модель {MODEL_PATH} не найдена \n"
            )
        
        self.session = ort.InferenceSession(str(MODEL_PATH))
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, features: list) -> float:
        """
        Обращение к сервису.
        """
        data = np.array([features], dtype=np.float32)
        result = self.session.run(None, {self.input_name: data})
        return float(result[0][0])
