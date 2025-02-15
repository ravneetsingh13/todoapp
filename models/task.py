from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the task")
    deadline: date = Field(..., description="Deadline date for the task")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the task")

    @validator('deadline')
    def deadline_must_be_future(cls, v):
        """Validate that deadline is not in the past"""
        if v < date.today():
            raise ValueError('Deadline cannot be in the past')
        return v

class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    deadline: Optional[date] = None
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

    @validator('deadline')
    def deadline_must_be_future(cls, v):
        """Validate that deadline is not in the past"""
        if v and v < date.today():
            raise ValueError('Deadline cannot be in the past')
        return v

class Task(BaseModel):
    """Schema for task response"""
    id: int
    name: str
    deadline: date
    description: Optional[str] = None
    created_at: datetime
    completed: bool = False
    
    class Config:
        """Pydantic config"""
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class TaskList(BaseModel):
    """Schema for list of tasks response"""
    tasks: List[Task]
    total_count: int