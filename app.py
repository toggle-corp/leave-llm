from fastapi import FastAPI
from pydantic import BaseModel

from leave_prompt import leave_request_parser


class Item(BaseModel):
    leave_request: str


app = FastAPI()


@app.get("/")
async def home():
    return {"result": "Welcome to my app"}


@app.post("/leave/")
async def create_item(item: Item):
    leave_requests = item.leave_request
    # return {"leave_request": item.leave_request}
    return leave_request_parser.parse_dates(leave_requests)
