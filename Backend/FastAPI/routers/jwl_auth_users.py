from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACSSES_TOKEN_EXPIRE_MINUTES = 1

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    password: str

users_db = {
    "dashvar": {
        "username": "dashvar",
        "full_name": "Dasha Var",
        "email": "dash@var.com",
        "disabled": False,
        "password": "$2a$12$AptIyJI/W85UQHy6/Tav1eBh1h9rm.BB8eub0IhZx/uxPgJZCfKPa"
        },
    "katyalin": {
        "username": "katyalin",
        "full_name": "Katya Lin",
        "email": "kat@lin.com",
        "disabled": True,
        "password": "$2a$12$Prs58Yq/2JNZE5nqBjncWuPHLdOcIAq.EYa.gfUHvHv.K0cgAj5hC"
        },
}

def search_user_db(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    return None

app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}