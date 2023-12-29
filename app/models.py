from pydantic import BaseModel

class Prompt(BaseModel):
    text: str

class Player(BaseModel):
    id: int
    name: str
    prompt_ids: list[int]

class Score(BaseModel):
    player_id: int
    points: int

