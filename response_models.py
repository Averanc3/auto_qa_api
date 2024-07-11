from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class ResourceRequest(BaseModel):
    id_: int = Field(alias="id", strict=True)
    project_tasks_resource_id: int
    volume: float
    cost: float
    batch_number: Optional[int] = None
    batch_parent_request_id: Optional[int] = None
    is_over_budget: bool
    created_at: int
    updated_at: int
    user_id: int
    needed_at: int
    created_by: int

    @field_validator("created_at", "updated_at")
    @classmethod
    def datetime_must_be_in_past(cls, value: int):
        dt = datetime.utcfromtimestamp(value)
        if dt >= datetime.utcnow():
            raise ValueError("Datetime must be in the past")
        return value

    @field_validator("id_")
    @classmethod
    def id_must_be_7_chars(cls, value: int):
        if len(str(value)) < 7:
            raise ValueError("ID less than 7 chars")
        return value


class ResourceRequestResponse(BaseModel):
    project_tasks: List[ResourceRequest]
