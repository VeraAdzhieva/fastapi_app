
from pydantic import BaseModel, Field
from fastapi import APIRouter
from src.application.commands import Predict
from src.application.handlers import (
    PredictHandler,
)

from src.infrastructure.auth.dependencies import CurrentUser

router = APIRouter(prefix="/predict", tags=["Predict"])

class PredictDTO(BaseModel):
    pregnancies: int = Field(..., description="Кол-во беременностей")
    glucose: int = Field(..., description="Уровень глюкозы")
    bmi: float = Field(..., description="Индекс массы тела")
    age: int = Field(..., description="Возраст")


@router.post("/predict", summary="Узнать наличие диабета", tags=["Predict"])
def has_diabet(
    dto: PredictDTO, user_info: CurrentUser,
) -> dict[str, str | float]:
    handler = PredictHandler()
    cmd = Predict(**dto.dict())
    try:
        result = handler(cmd, user_info)
        if result > 0.5:
            msg = "Есть вероятность диабета"
        else:
            msg = "Нет вероятности диабета"

        return {"message": msg, "user": user_info.username, "prediction": result}
    except Exception as e:
        return {"message": str(e)}