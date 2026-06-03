import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

from src.application.handlers import (
    PredictHandler,
)

from src.application.commands import (
   Predict
)

app = FastAPI(title="ONNX Prediction")
security = HTTPBasic()


def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
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
    Pregnancies: int = Field(..., description="Кол-во беременностей")
    Glucose: int = Field(..., description="Уровень глюкозы")
    BMI: float = Field(..., description="Индекс массы тела")
    Age: int = Field(..., description="Возраст")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from a unique FastAPI app!"}


@app.get("/secure")
def secure_area(username: str = Depends(verify_user)):
    return {"message": f"Welcome {username}, this is a protected route."}


@app.post("/predict", summary="Узнать наличие диабета", tags=["Predict"])
def has_diabet(dto: PredictDTO):
    handler = PredictHandler()
    cmd = Predict(**dto.dict())
    try:
        result = handler(cmd)
        
        return {"message": f"Возможность диабета: {result}"}
    except ValueError as e:
        return {"message": str(e)}