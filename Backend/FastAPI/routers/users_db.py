from fastapi import APIRouter, HTTPException, status
from db.models.user import User

router = APIRouter(prefix="/usersdb",
                   tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "No encontrado"}})

# Inicia el server:  uvicorn users_db:app --reload

users_list = []

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

@router.post("/", status_code=status.HTTP_201_CREATED)
async def user(user: User):
    print(user)
    print(user.id)
    if type(search_user(user.id)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
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
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Error user not found")
