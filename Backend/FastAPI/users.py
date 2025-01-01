from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Inicia el server:  uvicorn users:app --reload

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User( id=1, name="Dasha", surname="Boch", url="https://www.linkedin.com/in/dasha-boch/", age=25),
    User( id=2, name="Katya", surname="Lin", url="https://www.linkedin.com/in/katya-lin/", age=55),
    User( id=3, name="Misty", surname="Pep", url="https://www.linkedin.com/in/misty-pep/", age=35)
]
   
   
@app.get("/usersjson")
async def usersjson():
    return [{"name": "Dasha", "surname": "Boch", "url": "https://www.linkedin.com/in/dasha-boch/", "age": 25},
            {"name": "Katya", "surname": "Lin", "url": "https://www.linkedin.com/in/katya-lin/", "age": 55},
            {"name": "Misty", "surname": "Pep", "url": "https://www.linkedin.com/in/misty-pep/", "age": 35}]


@app.get("/users")
async def users():
    return users_list


#Path

@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#Query

@app.get("/user/")
async def user(id: int):
    return search_user(id)

@app.post("/user/")
async def user(user: User):
    print(user)
    print(user.id)
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)
        return user
    
@app.put("/user/")
async def user(user: User):

        found =False

        for index, saved_user in enumerate(users_list):
            if saved_user.id == user.id:
                users_list[index] = user
                return user
        if not found:
            return {"error": "El usuario no se actualizado"}
        else:
            return user

@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

        if not found:
            return {"error": "El usuario no se ha eliminado"}   

def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        return {"error": "Error user not found"}
    
