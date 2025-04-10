import uuid
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class ProcessingStatus(Enum):
    NEW = "new"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"


class Task(BaseModel):
    user_id: str
    description: str | None = None


class TaskManagement:
    def __init__(self):
        self.tasks = []

    def create_task(self, user_id, description):
        event = {
            "user_id": user_id,
            "description": description,
            "id": str(uuid.uuid4()),
            "status": ProcessingStatus.NEW.value
        }

        self.tasks.append(event)
        return event

    def retrieve_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task

    def retrieve_tasks(self, status=None):
        if status:
            return [task for task in self.tasks if task["status"] == status]

        return self.tasks


task_management = TaskManagement()


@app.get("/tasks/{task_id}")
def retrieve_task(task_id: str):
    event = task_management.retrieve_task(task_id)
    return event


@app.get("/tasks")
def retrieve_tasks(status: Optional[ProcessingStatus] = Query(None)):
    return task_management.retrieve_tasks(status.value if status else None)


@app.post('/tasks')
def create_task(task: Task):
    event = task_management.create_task(task.user_id, task.description)
    return event
