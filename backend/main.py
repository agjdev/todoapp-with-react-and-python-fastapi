from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware

# App object
app = FastAPI()
from database import (
    fetch_one_todo,
    fetch_all_todo,
    create_todo,
    update_todo,
    remove_todo
)

from model import Todo

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def index():
    return {"ping": "pong"}

@app.get("/api/todo", response_model=list[Todo])
async def get_all_todos():
    response = await fetch_all_todo()
    return response

@app.get("/api/todo/{title}", response_model=Todo)
async def get_single_todo(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"there is no todo item with this title {title}")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.model_dump())
    if response:
        return response
    raise HTTPException(400, "Bad request")

@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title: str, todo: Todo):
    response = await update_todo(title, todo.description)
    if response:
        return response
    raise HTTPException(404, f"there is no todo item with this title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "successfully deleted"
    raise HTTPException(404, f"there is no todo item with this title {title}")