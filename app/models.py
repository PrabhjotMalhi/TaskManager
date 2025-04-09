from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    deadline: datetime
    created_at: datetime = None
    completed: bool = False

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False
