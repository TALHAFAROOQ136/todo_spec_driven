from todo_app.store import TaskStore


def display_menu() -> None:
    print("\n===== Todo App =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Exit")
    print("====================")


def get_task_id_input() -> int:
    while True:
        try:
            task_id = int(input("Enter task ID: "))
            if task_id <= 0:
                print("Please enter a positive number.")
                continue
            return task_id
        except ValueError:
            print("Invalid input. Please enter a number.")


def handle_add(store: TaskStore) -> None:
    while True:
        title = input("Enter task title: ").strip()
        if title:
            break
        print("Title cannot be empty.")
    description = input("Enter task description (optional): ")
    task = store.add(title, description)
    print(f"Task {task.id} created: {task.title}")


def handle_view(store: TaskStore) -> None:
    tasks = store.get_all()
    if not tasks:
        print("No tasks found.")
        return
    print(f"\n{'ID':<5} {'Status':<8} {'Title':<30} {'Description'}")
    print("-" * 70)
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        print(f"{task.id:<5} {status:<8} {task.title:<30} {task.description}")


def handle_toggle(store: TaskStore) -> None:
    task_id = get_task_id_input()
    task = store.toggle_complete(task_id)
    if task is None:
        print("Task not found.")
    elif task.completed:
        print(f"Task {task.id} marked as complete.")
    else:
        print(f"Task {task.id} marked as incomplete.")


def handle_update(store: TaskStore) -> None:
    task_id = get_task_id_input()
    new_title = input("Enter new title (press Enter to skip): ")
    new_description = input("Enter new description (press Enter to skip): ")
    title = new_title if new_title else None
    description = new_description if new_description else None
    if title is None and description is None:
        print("No changes provided.")
        return
    try:
        task = store.update(task_id, title=title, description=description)
    except ValueError as e:
        print(str(e))
        return
    if task is None:
        print("Task not found.")
    else:
        print(f"Task {task.id} updated: {task.title}")


def handle_delete(store: TaskStore) -> None:
    task_id = get_task_id_input()
    task = store.delete(task_id)
    if task is None:
        print("Task not found.")
    else:
        print(f"Task {task.id} deleted.")


def main() -> None:
    store = TaskStore()
    print("Welcome to Todo App!")

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_add(store)
        elif choice == "2":
            handle_view(store)
        elif choice == "3":
            handle_update(store)
        elif choice == "4":
            handle_delete(store)
        elif choice == "5":
            handle_toggle(store)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
