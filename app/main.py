from fastapi import FastAPI
from models import *
from database import *

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Define your API endpoints here
@app.post("/prompts/")
async def create_prompt(prompt: Prompt):
    query = prompts.insert().values(text=prompt.text)
    last_record_id = await database.execute(query)
    return {**prompt.dict(), "id": last_record_id}

# Add more endpoints...

@app.get("/prompts/")
async def read_prompts():
    query = prompts.select()
    return await database.fetch_all(query)

