# app/main.py
from task_manager import TaskManager
from command import CreateTaskCommand, ListTasksCommand
from datetime import datetime

manager = TaskManager()
manager.setup()

while True:
    print("\n1. Create Task\n2. List Tasks\n3. Exit")
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
    else:
        break