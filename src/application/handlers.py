from src.application.commands import Predict
from src.infrastructure.models.onnx_service import OnnxPredict

predictor = OnnxPredict()


class PredictHandler:
    def __call__(self, cmd: Predict) -> float:
        """
        Вероятность диабета.
        """
        features = cmd.to_features_array()
        result = predictor.predict(features)

        return result
