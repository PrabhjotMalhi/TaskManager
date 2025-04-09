from datetime import datetime
from models import Task
from typing import Optional

class TaskFactory:
    @staticmethod
    def create_task(
        title: str,
        description: str,
        deadline: datetime,
        task_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        completed: bool = False
    ) -> Task:
        return Task(
            id=task_id,
            title=title,
            description=description,
            deadline=deadline,
            created_at=created_at,
            completed=completed
        )
