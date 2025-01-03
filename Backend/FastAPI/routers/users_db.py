from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/usersdb",
                   tags=["usersdb"],
                   responses={404: {"description": "No encontrado"}})

# Inicia el server:  uvicorn users_db:app --reload

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

@router.get("/")
async def users():
    return users_list


#Path

@router.get("/{id}")
async def user(id: int):
    return search_user(id)

#Query

@router.get("/")
async def user(id: int):
    return search_user(id)

@router.post("/", status_code=201)
async def user(user: User):
    print(user)
    print(user.id)
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user
    
@router.put("/")
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

@router.delete("/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "El usuario no se  ha actualizado"}   

def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Error user not found")
