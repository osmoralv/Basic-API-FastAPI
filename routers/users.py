from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "NOT FOUND"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/user/{id}")
async def user(id: str):
    user = search_user("_id", ObjectId(id)) 
    return user                                                                                                                                 


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email" , user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="This user already exist")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/user/{id}")
async def user(user: User):
    user_dict = dict(user)
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"error": "User Not Found"}
    
    return search_user("_id", ObjectId(user.id))


@router.delete("/user/{id}")
async def user(id: str):
    try:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    except:
        return {"error": "User Not Found"}


def search_user(field, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "User Not Found"}