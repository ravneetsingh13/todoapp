from datetime import datetime
from typing import Dict, List

# Simple in-memory storage
class Database:
    def __init__(self):
        self.tasks: Dict[int, dict] = {}
        self.counter = 1

    def create_task(self, task_data: dict) -> dict:
        """Create a new task"""
        task = {
            "id": self.counter,
            "name": task_data["name"],
            "deadline": task_data["deadline"],
            "description": task_data.get("description"),
            "created_at": datetime.utcnow(),
            "completed": False
        }
        self.tasks[self.counter] = task
        self.counter += 1
        return task

    def get_task(self, task_id: int) -> dict:
        """Get a task by id"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[dict]:
        """Get all tasks"""
        return list(self.tasks.values())

    def update_task(self, task_id: int, task_data: dict) -> dict:
        """Update a task"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        for key, value in task_data.items():
            if value is not None:
                task[key] = value
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

# Create a global instance
db = Database()