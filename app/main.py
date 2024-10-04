from fastapi import FastAPI
from api.routes.todo import todo_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.include_router(todo_router)
register_tortoise(
    app=app,
    db_url="sqlite://todos.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"modules": ["api.models.todo"]}
)

@app.get("/")
def index():
    return {"Status": "todo api is running"}