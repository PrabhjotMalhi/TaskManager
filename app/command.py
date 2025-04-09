from datetime import datetime
from abc import ABC, abstractmethod
from task_manager import TaskManager

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CreateTaskCommand(Command):
    def __init__(self, task_manager: TaskManager, title: str, description: str, deadline: datetime):
        self.task_manager = task_manager
        self.title = title
        self.description = description
        self.deadline = deadline

    def execute(self):
        self.task_manager.create_task(self.title, self.description, self.deadline)
        print("Task created successfully!")

class ListTasksCommand(Command):
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def execute(self):
        tasks = self.task_manager.list_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print("\nCurrent Tasks:")
        print("-" * 50)
        for task in tasks:
            status = "✓" if task.completed else " "
            print(f"[{status}] {task.title}")
            print(f"    Description: {task.description}")
            print(f"    Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 50)
