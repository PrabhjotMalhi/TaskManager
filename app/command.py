from datetime import datetime
from abc import ABC, abstractmethod
from task_manager import TaskManager

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CreateTaskCommand(Command):
    def __init__(self, manager: TaskManager, title: str, description: str, deadline: datetime):
        self.manager = manager
        self.title = title
        self.description = description
        self.deadline = deadline

    def execute(self):
        task = self.manager.create_task(self.title, self.description, self.deadline)
        print(f"\nTask created successfully with ID: {task.id}")

class ListTasksCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        tasks = self.manager.list_tasks()
        if not tasks:
            print("\nNo tasks found.")
            return

        print("\nTasks:")
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            print(f"\nID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Deadline: {task.deadline}")
            print(f"Status: {status}")

class EditTaskCommand(Command):
    def __init__(self, manager: TaskManager, task_id: int, title: str, description: str, deadline: datetime):
        self.manager = manager
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline

    def execute(self):
        success = self.manager.edit_task(self.task_id, self.title, self.description, self.deadline)
        if success:
            print(f"\nTask {self.task_id} updated successfully!")
        else:
            print(f"\nFailed to update task {self.task_id}. Task not found.")

class DeleteTaskCommand(Command):
    def __init__(self, manager: TaskManager, task_id: int):
        self.manager = manager
        self.task_id = task_id

    def execute(self):
        success = self.manager.delete_task(self.task_id)
        if success:
            print(f"\nTask {self.task_id} deleted successfully!")
        else:
            print(f"\nFailed to delete task {self.task_id}. Task not found.")
