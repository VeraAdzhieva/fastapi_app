import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from .admin import router as admin
from .predict import router as predict
from .users import router as users

app = FastAPI(title="ONNX Prediction")
security = HTTPBearer()


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


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from a unique FastAPI app!"}


app.include_router(users)
app.include_router(admin)
app.include_router(predict)
