import sqlite3
from datetime import datetime, date
from typing import List, Optional
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_name: str = "todo.db"):
        """Initialize database manager"""
        self.db_name = db_name
        # Delete existing database to apply new schema
        try:
            import os
            if os.path.exists(db_name):
                os.remove(db_name)
        except:
            pass
        self.init_db()

    @contextmanager
    def get_db_cursor(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn.cursor()
            conn.commit()
        finally:
            conn.close()

    def init_db(self):
        """Initialize database tables"""
        with self.get_db_cursor() as cursor:
            # Create tasks table with all required columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    deadline DATE NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    completed_at TIMESTAMP
                )
            ''')

    def create_task(self, task_data: dict) -> dict:
        """Create a new task"""
        with self.get_db_cursor() as cursor:
            cursor.execute('''
                INSERT INTO tasks (name, description, deadline, created_at, completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                task_data["name"],
                task_data.get("description"),
                task_data["deadline"].isoformat(),
                datetime.utcnow().isoformat(),
                False,
                None
            ))
            
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (cursor.lastrowid,))
            return dict(cursor.fetchone())

    def get_task(self, task_id: int) -> Optional[dict]:
        """Get a task by ID"""
        with self.get_db_cursor() as cursor:
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_tasks(self, completed: Optional[bool] = None) -> List[dict]:
        """
        Get all tasks with optional completed filter
        Args:
            completed: If provided, filter tasks by completion status
        """
        with self.get_db_cursor() as cursor:
            if completed is None:
                cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            else:
                cursor.execute(
                    'SELECT * FROM tasks WHERE completed = ? ORDER BY created_at DESC',
                    (completed,)
                )
            return [dict(row) for row in cursor.fetchall()]

    def update_task(self, task_id: int, task_data: dict) -> Optional[dict]:
        """Update a task"""
        update_fields = []
        values = []
        
        # Handle completion status specially to update completed_at
        if 'completed' in task_data:
            update_fields.extend(['completed = ?', 'completed_at = ?'])
            values.append(task_data['completed'])
            values.append(
                datetime.utcnow().isoformat() if task_data['completed'] else None
            )
            del task_data['completed']

        # Handle other fields
        for key, value in task_data.items():
            if value is not None:
                update_fields.append(f"{key} = ?")
                if isinstance(value, date):
                    value = value.isoformat()
                values.append(value)

        if not update_fields:
            return self.get_task(task_id)

        values.append(task_id)
        update_query = f'''
            UPDATE tasks 
            SET {", ".join(update_fields)}
            WHERE id = ?
        '''

        with self.get_db_cursor() as cursor:
            cursor.execute(update_query, values)
            if cursor.rowcount == 0:
                return None
            
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            return dict(cursor.fetchone())

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with self.get_db_cursor() as cursor:
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            return cursor.rowcount > 0

    def get_completed_tasks(self) -> List[dict]:
        """Get all completed tasks ordered by completion date"""
        with self.get_db_cursor() as cursor:
            cursor.execute('''
                SELECT * FROM tasks 
                WHERE completed = 1 
                ORDER BY completed_at DESC NULLS LAST
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def convert_row_to_dict(self, row: sqlite3.Row) -> dict:
        """Convert a SQLite Row to a dictionary with proper date/datetime parsing"""
        if row is None:
            return None
            
        task_dict = dict(row)
        if 'deadline' in task_dict:
            task_dict['deadline'] = date.fromisoformat(task_dict['deadline'])
        if 'created_at' in task_dict:
            task_dict['created_at'] = datetime.fromisoformat(task_dict['created_at'])
        if 'completed_at' in task_dict and task_dict['completed_at']:
            task_dict['completed_at'] = datetime.fromisoformat(task_dict['completed_at'])
        return task_dict