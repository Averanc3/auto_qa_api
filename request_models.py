from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjectTaskRequestBody(BaseModel):
    model_config = ConfigDict(extra="allow")
    project_tasks_resource_id: int
    needed_at: int
    volume: int
    is_over_budget: Optional[int] = 0
