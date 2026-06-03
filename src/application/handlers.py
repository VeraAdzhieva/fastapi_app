from src.application.commands import Predict

from infrastructure.models.onnx_service import OnnxPredict

predictor = OnnxPredict()

class PredictHandler:
    """
    Вероятность диабета.
    """

    def __init__(self):
        ...

    def __call__(self, cmd: Predict) -> bool:
        features = cmd.to_features_array()
        result = predictor.predict(features)
        if result > 0.5:
            return "Да"
        else: return "Нет"