from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    password: str

users_db = {
    "dashboch": {
        "username": "dashvar",
        "full_name": "Dasha Var",
        "email": "dash@var.com",
        "disabled": False,
        "password": "123456"
        },
    "katyalin": {
        "username": "katyalin",
        "full_name": "Katya Lin",
        "email": "kat@lin.com",
        "disabled": True,
        "password": "123457"
        },
}

def search_user(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    return None
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación no válidas",
            headers={"WWW-Authenticate": "Bearer"},)
    return user
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no es correcto")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="Contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user