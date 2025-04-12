from datetime import datetime
from db_handler import DatabaseHandler
from calendar_adapter import CalendarAdapter
from task_factory import TaskFactory
import pytz

class TaskManager:
    def __init__(self):
        self.db = DatabaseHandler()
        self.calendar = CalendarAdapter()
        self.task_factory = TaskFactory()
        self.timezone = pytz.timezone('America/New_York')

    def setup(self):
        """Initialize the database connection"""
        self.db.connect()

    def create_task(self, title: str, description: str, deadline: datetime):
        """Create a new task and save it to the database"""
        # Convert naive datetime to EST timezone
        if deadline.tzinfo is None:
            deadline = self.timezone.localize(deadline)
            
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

    def edit_task(self, task_id: int, title: str = None, description: str = None, deadline: datetime = None) -> bool:
        """Edit an existing task"""
        tasks = self.db.get_all_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if deadline:
                # Convert naive datetime to EST timezone if needed
                if deadline.tzinfo is None:
                    deadline = self.timezone.localize(deadline)
                task.deadline = deadline
            
            # Update in database
            self.db.update_task(task)
            
            # Update in calendar
            self.calendar.remove_task_from_calendar(task_id)
            self.calendar.add_task_to_calendar(task)
            
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            self.db.delete_task(task_id)
            self.calendar.remove_task_from_calendar(task_id)
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False

    def __del__(self):
        """Cleanup database connection"""
        try:
            self.db.close()
        except:
            pass
