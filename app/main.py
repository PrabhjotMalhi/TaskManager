# app/main.py
from task_manager import TaskManager
from command import CreateTaskCommand, ListTasksCommand, EditTaskCommand, DeleteTaskCommand
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

manager = TaskManager()
manager.setup()

while True:
    print("\n1. Create Task\n2. List Tasks\n3. Edit Task\n4. Delete Task\n5. Exit")
    choice = input("Select option: ")

    if choice == '1':
        title = input("Title: ")
        desc = input("Description: ")
        deadline = input("Deadline (YYYY-MM-DD HH:MM): ")
        dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        cmd = CreateTaskCommand(manager, title, desc, dt)
        cmd.execute()
    elif choice == '2':
        cmd = ListTasksCommand(manager)
        cmd.execute()
    elif choice == '3':
        cmd = ListTasksCommand(manager)
        cmd.execute()
        task_id = int(input("\nEnter Task ID to edit: "))
        title = input("New Title (press Enter to keep current): ")
        desc = input("New Description (press Enter to keep current): ")
        deadline = input("New Deadline (YYYY-MM-DD HH:MM, press Enter to keep current): ")
        dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M") if deadline else None
        cmd = EditTaskCommand(manager, task_id, title, desc, dt)
        cmd.execute()
    elif choice == '4':
        cmd = ListTasksCommand(manager)
        cmd.execute()
        task_id = int(input("\nEnter Task ID to delete: "))
        cmd = DeleteTaskCommand(manager, task_id)
        cmd.execute()
    else:
        break