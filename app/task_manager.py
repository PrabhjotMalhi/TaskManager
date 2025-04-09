from datetime import datetime
from db_handler import DatabaseHandler
from calendar_adapter import CalendarAdapter
from task_factory import TaskFactory

class TaskManager:
    def __init__(self):
        self.db = DatabaseHandler()
        self.calendar = CalendarAdapter()
        self.task_factory = TaskFactory()

    def setup(self):
        """Initialize the database connection"""
        self.db.connect()

    def create_task(self, title: str, description: str, deadline: datetime):
        """Create a new task and save it to the database"""
        task = self.task_factory.create_task(
            title=title,
            description=description,
            deadline=deadline
        )
        
        # Save to database
        task.id = self.db.add_task(task)
        
        # Add to calendar
        self.calendar.add_task_to_calendar(task)
        
        return task

    def list_tasks(self):
        """Retrieve all tasks from the database"""
        return self.db.get_all_tasks()

    def mark_task_complete(self, task_id: int):
        """Mark a task as complete"""
        tasks = self.db.get_all_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            task.mark_complete()
            self.db.update_task(task)
            return True
        return False

    def delete_task(self, task_id: int):
        """Delete a task"""
        self.db.delete_task(task_id)
        self.calendar.remove_task_from_calendar(task_id)

    def __del__(self):
        """Cleanup database connection"""
        try:
            self.db.close()
        except:
            pass
