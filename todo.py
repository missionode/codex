import os
import questionary
from task_manager import TaskManager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_tasks(tasks):
    if not tasks:
        print("No tasks yet! Add one by typing its description.")
        return

    print("\n--- Your Tasks ---")
    for i, task in enumerate(tasks, 1):
        status = "[x]" if task['completed'] else "[ ]"
        print(f"{status} {i}: {task['description']}")
    print("------------------\n")

def main():
    task_manager = TaskManager()

    while True:
        clear_screen()
        display_tasks(task_manager.get_tasks())

        try:
            user_input = questionary.text("Enter a command or a new task:").ask()
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            user_input = "/exit"

        if not user_input:
            continue

        if user_input.startswith('/'):
            command_parts = user_input.split(' ', 1)
            command = command_parts[0].lower()

            if command == '/exit':
                print("Exiting Todo application. Goodbye!")
                break
            elif command == '/complete':
                tasks = task_manager.get_tasks()
                if not tasks:
                    input("No tasks to complete. Press Enter to continue.")
                    continue
                
                choices = [
                    questionary.Choice(
                        title=f"{'[x]' if task['completed'] else '[ ]'} {i}: {task['description']}",
                        value=task['id']
                    ) for i, task in enumerate(tasks, 1)
                ]
                
                task_id_to_toggle = questionary.select(
                    "Select a task to toggle completion:",
                    choices=choices
                ).ask()

                if task_id_to_toggle is not None:
                    task = next((t for t in tasks if t['id'] == task_id_to_toggle), None)
                    if task:
                        new_status = not task['completed']
                        task_manager.update_task(task_id_to_toggle, completed=new_status)
                        status_text = "complete" if new_status else "incomplete"
                        input(f"Task marked as {status_text}. Press Enter to continue.")
                else:
                    input("No task selected. Press Enter to continue.")

            elif command == '/delete':
                tasks = task_manager.get_tasks()
                if not tasks:
                    input("No tasks to delete. Press Enter to continue.")
                    continue

                choices = [
                    questionary.Choice(
                        title=f"{'[x]' if task['completed'] else '[ ]'} {i}: {task['description']}",
                        value=task['id']
                    ) for i, task in enumerate(tasks, 1)
                ]

                task_id_to_delete = questionary.select(
                    "Select a task to delete:",
                    choices=choices
                ).ask()

                if task_id_to_delete is not None:
                    if questionary.confirm(f"Are you sure you want to delete this task?").ask():
                        task_manager.delete_task(task_id_to_delete)
                        input(f"Task deleted. Press Enter to continue.")
                    else:
                        input("Deletion cancelled. Press Enter to continue.")
                else:
                    input("No task selected. Press Enter to continue.")

            elif command == '/edit':
                tasks = task_manager.get_tasks()
                if not tasks:
                    input("No tasks to edit. Press Enter to continue.")
                    continue

                choices = [
                    questionary.Choice(
                        title=f"{'[x]' if task['completed'] else '[ ]'} {i}: {task['description']}",
                        value=task['id']
                    ) for i, task in enumerate(tasks, 1)
                ]

                task_id_to_edit = questionary.select(
                    "Select a task to edit:",
                    choices=choices
                ).ask()

                if task_id_to_edit is not None:
                    current_task = next((task for task in tasks if task['id'] == task_id_to_edit), None)
                    if current_task:
                        new_description = questionary.text(
                            "Enter the new description:",
                            default=current_task['description']
                        ).ask()
                        if new_description and new_description != current_task['description']:
                            task_manager.update_task(task_id_to_edit, description=new_description)
                            input(f"Task updated. Press Enter to continue.")
                        else:
                            input("Edit cancelled or no changes made. Press Enter to continue.")
                else:
                    input("No task selected. Press Enter to continue.")

            elif command == '/flush':
                if questionary.confirm("Are you sure you want to remove all completed tasks?").ask():
                    if task_manager.flush_completed_tasks():
                        input("All completed tasks have been removed. Press Enter to continue.")
                    else:
                        input("No completed tasks to remove. Press Enter to continue.")
                else:
                    input("Flush cancelled. Press Enter to continue.")
            else:
                input(f"Unknown command: {command}. Press Enter to continue.")
        else:
            # Default action: add a new task
            task_manager.add_task(user_input)
            input(f"Task '{user_input}' added. Press Enter to continue.")

if __name__ == '__main__':
    main()
