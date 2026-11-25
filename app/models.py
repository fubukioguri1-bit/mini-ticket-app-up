from typing import Literal
from pydantic import BaseModel, Field, field_validator

StatusType = Literal["TODO", "DOING", "DONE"]


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    assignee: str = Field(..., min_length=1, max_length=50)

    @field_validator("title", "assignee")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("空白のみの入力は許可されていません")
        return v.strip()


class TicketStatusUpdate(BaseModel):
    status: StatusType


class TicketResponse(BaseModel):
    id: int
    title: str
    assignee: str
    status: StatusType
    created_at: str