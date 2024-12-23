from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Inicia el server:  uvicorn users:app --reload

#Entidad user
class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Dasha", "surname": "Boch", "url": "https://www.linkedin.com/in/dasha-boch/", "age": 25},
            {"name": "Katya", "surname": "Lin", "url": "https://www.linkedin.com/in/katya-lin/", "age": 55},
            {"name": "Misty", "surname": "Pep", "url": "https://www.linkedin.com/in/misty-pep/", "age": 35}]


@app.get("/usersclass")
async def usersclass():
    return User(name="Dasha", surname="Boch", url="https://www.linkedin.com/in/dasha-boch/", age=25)