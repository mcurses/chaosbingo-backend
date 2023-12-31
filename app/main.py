from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Set

from models import *
from database import *

app = FastAPI()

# Set up CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# A set to hold active WebSocket connections
active_connections: Set[WebSocket] = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back received message or handle as needed
            # ...
    except Exception as e:
        # Handle disconnection or errors
        pass
    finally:
        active_connections.remove(websocket)


async def broadcast_prompts():
    prompt_records = await read_prompts()  # Fetch prompts from the database

    # Convert database rows to a list of dictionaries
    prompts = [{"id": record.id, "title": record.title, "description": record.description} for record in prompt_records]

    for connection in active_connections:
        await connection.send_json(prompts)  # Send the serialized prompts as JSON


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/prompts/")
async def create_prompt(prompt: Prompt):
    query = prompts.insert().values(title=prompt.title, description=prompt.description)
    last_record_id = await database.execute(query)
    await broadcast_prompts()  # After adding a new prompt, broadcast the update
    return {**prompt.dict(), "id": last_record_id}


@app.delete("/prompts/delete/{prompt_id}")
async def delete_prompt(prompt_id: int):
    query = prompts.delete().where(prompts.c.id == prompt_id)
    await database.execute(query)
    await broadcast_prompts()  # Broadcast update after deletion
    return {"message": "Prompt deleted successfully"}


@app.get("/prompts/")
async def read_prompts():
    query = prompts.select()
    return await database.fetch_all(query)
