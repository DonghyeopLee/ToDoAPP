from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist
from api.models.todo import Todo
from api.schemas.todo import GetTodo, PostTodo, PutTodo

todo_router = APIRouter(prefix="/api", tags=["Todo"])

@todo_router.get("/")
async def all_todos():
    try:
        data = await Todo.all()
        return await GetTodo.from_queryset(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@todo_router.post("/")
async def post_todo(body: PostTodo):
    try:
        data = body.dict(exclude_unset=True)  # Use dict() to get a dictionary
        row = await Todo.create(**data)
        return await GetTodo.from_tortoise_orm(row)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@todo_router.put("/{key}")
async def update_todo(key: int, body: PutTodo):
    try:
        data = body.model_dump(exclude_unset=True)  # Use model_dump() to get a dictionary
        exists = await Todo.filter(id=key).exists()
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        await Todo.filter(id=key).update(**data)
        updated_todo = await Todo.get(id=key)
        return await GetTodo.from_tortoise_orm(updated_todo)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@todo_router.delete("/{key}")
async def delete_todo(key: int):
    try:
        exists = await Todo.filter(id=key).exists()
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        await Todo.filter(id=key).delete()
        return {"detail": "Todo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
