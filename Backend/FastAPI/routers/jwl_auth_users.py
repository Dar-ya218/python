from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACSSES_TOKEN_DURATION = 1
SECRET = "bce92d49cfcf02fa6fdf836d91c00c01702894340bbca263e89f835b2accea5e"

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

def search_user(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    return None

async def auth_user(tocken: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación no válidas",
            headers={"WWW-Authenticate": "Bearer"},)

    try:
        username = jwt.decode(tocken, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
        
    return  search_user(username)

async def current_user(user: User = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    
    return user

@app.post("/login")
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

    access_token = {"sub":user.username, 
                    "exp":datetime.utcnow() + timedelta(minutes=ACSSES_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user