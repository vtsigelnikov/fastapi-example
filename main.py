from datetime import date, datetime
from enum import StrEnum
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field, StringConstraints, field_validator

app = FastAPI()

StripStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        strip_whitespace=True,
    ),
]

BANNED_WORDS = ["test"]


class Q(StrEnum):
    FOO = "foo"
    BOO = "boo"


class Input(BaseModel):
    name: Q
    description: StripStr | None = Field(default=None, description="The description of the item")
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    created_at: datetime

    @field_validator("name")
    @classmethod
    def check_banned_words(cls, v: str) -> str:
        if v in BANNED_WORDS:
            error_message = "name contains banned words"
            raise ValueError(error_message)
        return v


class Output(BaseModel):
    id: int
    name: str
    description: str
    price: float
    tax: float
    created_at: date

@app.put(
    path="/items/{item_id}",
    response_model=Output,
    responses={404: {"description": "Item not found"}}
)
async def update_item(item_id: Q, body: Input, q: Q | None = None) -> Output:
    result = {"id": item_id, **body.model_dump()}
    return Output(**result)
