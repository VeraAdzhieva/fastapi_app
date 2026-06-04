import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

from src.application.commands import Predict
from src.application.handlers import (
    PredictHandler,
)

app = FastAPI(title="ONNX Prediction")
security = HTTPBasic()


def verify_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(credentials.username, "demo_user")
    correct_password = secrets.compare_digest(credentials.password, "demo_pass")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class PredictDTO(BaseModel):
    pregnancies: int = Field(..., description="Кол-во беременностей")
    glucose: int = Field(..., description="Уровень глюкозы")
    bmi: float = Field(..., description="Индекс массы тела")
    age: int = Field(..., description="Возраст")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from a unique FastAPI app!"}


@app.get("/secure")
def secure_area(username: str = Depends(verify_user)) -> dict[str, str]:
    return {"message": f"Welcome {username}, this is a protected route."}


@app.post("/predict", summary="Узнать наличие диабета", tags=["Predict"])
def has_diabet(dto: PredictDTO, username: str = Depends(verify_user)) -> dict[str, str]:
    handler = PredictHandler()
    cmd = Predict(**dto.dict())
    try:
        result = handler(cmd)
        if result:
            msg = "Есть вероятность диабета"
        else:
            msg = "Нет вероятности диабета"

        return {"message": msg, "user": username}
    except Exception as e:
        return {"message": str(e)}
