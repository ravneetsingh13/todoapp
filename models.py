from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    """Schema for creating a new todo"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    priority: int = Field(default=1, ge=1, le=5)  # Priority from 1-5

class TodoUpdate(BaseModel):
    """Schema for updating an existing todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    completed: Optional[bool] = None

class Todo(BaseModel):
    """Schema for todo item response"""
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime
    due_date: Optional[datetime] = None
    priority: int
    completed: bool = False

class TodoList(BaseModel):
    """Schema for list of todos response"""
    todos: List[Todo]
    total_count: int