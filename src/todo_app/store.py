from todo_app.models import Task


class TaskStore:
    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_all(self) -> list[Task]:
        return list(self.tasks.values())

    def toggle_complete(self, task_id: int) -> Task | None:
        task = self.tasks.get(task_id)
        if task is None:
            return None
        task.completed = not task.completed
        return task

    def update(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None:
        task = self.tasks.get(task_id)
        if task is None:
            return None
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title cannot be empty.")
            task.title = title
        if description is not None:
            task.description = description
        return task

    def delete(self, task_id: int) -> Task | None:
        return self.tasks.pop(task_id, None)
