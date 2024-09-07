import os
import datetime
import json
import argparse


def json_check():
    # Check if the JSON file exists
    try:
        if not os.path.exists('tasks.json'):
            # If it doesn't exist, create and initialize it with an empty list
            with open('tasks.json', 'w') as tasks:
                json.dump([], tasks)
    except IOError as e:
        print(f"Error creating or writing to tasks.json: {e}")


def add_task(args):
    json_check()
    now = datetime.datetime.now()
    data = json_read()
    existing_ids = [task.get("id") for task in data]

    if existing_ids:
        existing_ids.sort()
        new_id = 1
        for id in existing_ids:
            if id != new_id:
                break
            new_id += 1
    else:
        new_id = 0
    json_data = {
        "id": new_id,
        "description": args.description,
        "status": "todo",
        "dates": {
            "created_at": now.strftime("%d/%m/%Y"),
            "modified_at": now.strftime("%d/%m/%Y"),
        }
    }
    data.append(json_data)
    with open('tasks.json', 'w') as tasks:
        json.dump(data, tasks, indent=2)
    print(f"Task {args.description} added with id {new_id}")


def json_read():
    json_check()
    with open('tasks.json', 'r') as tasks:
        try:
            return json.load(tasks)
        except json.JSONDecodeError:
            print("Invalid JSON file")


def print_custom(task):
    task_id = task.get("id", "N/A")
    description = task.get("description", "N/A")
    status = task.get("status", "N/A")
    created_at = task.get("dates", {}).get("created_at", "N/A")
    modified_at = task.get("dates", {}).get("modified_at", "N/A")

    print(f"ID: {task_id}\nDescription: {description}\nStatus: {status}\nCreated at: {created_at}\nModified at: {modified_at}\n")


def list_tasks(args=None):
    json_check()
    tasks = json_read()
    if args.status:
        filtered_tasks = [
            task for task in tasks if tasks["status"] == args.status]
        if filtered_tasks:
            for task in filtered_tasks:
                print_custom(task)
        else:
            print("No tasks found")
    else:
        for task in tasks:
            print_custom(task)


def delete_task(args):
    json_check()
    data = json_read()

    # Convert args.id to int if IDs are integers
    task_id = int(args.id)  # Ensure args.id is of the same type as task["id"]

    # Flag to check if the task was found and updated
    task_found = False

    for task in data:
        if task["id"] == task_id:
            data.remove(task)
            task_found = True
            break

    if not task_found:
        print(f"Task with id {task_id} not found")
        return

    # Write the updated data back to the file
    with open('tasks.json', 'w') as tasks:
        json.dump(data, tasks, indent=2)

    print(f"Task {args.id} deleted")


def mark(args):
    json_check()
    data = json_read()

    # Convert args.id to int if IDs are integers
    task_id = int(args.id)  # Ensure args.id is of the same type as task["id"]

    # Flag to check if the task was found and updated
    task_found = False

    for task in data:
        if task["id"] == task_id:
            task["status"] = args.status
            task_found = True
            break

    if not task_found:
        print(f"Task with id {task_id} not found")
        return

    # Write the updated data back to the file
    with open('tasks.json', 'w') as tasks:
        json.dump(data, tasks, indent=2)

    print(f"Task {task_id} marked as {args.status}")


def update(args):
    json_check()
    data = json_read()

    # Convert args.id to int if IDs are integers
    task_id = int(args.id)  # Ensure args.id is of the same type as task["id"]

    # Flag to check if the task was found and updated
    task_found = False

    for task in data:
        if task["id"] == task_id:
            task["description"] = args.description
            task_found = True
            break

    if not task_found:
        print(f"Task with id {task_id} not found")
        return

    # Write the updated data back to the file
    with open('tasks.json', 'w') as tasks:
        json.dump(data, tasks, indent=2)

    print(f"Task {task_id} marked as {args.description}")


def add_command_parser(subparsers, command, help_text, *args):
    """Helper function to add a subcommand parser."""
    parser = subparsers.add_parser(command, help=help_text)
    for arg in args:
        parser.add_argument(*arg[0], **arg[1])
    return parser


def main():
    json_check()
    command_options = {
        'list': list_tasks,
        'add': add_task,
        'delete': delete_task,
        'mark': mark,
        'update': update
    }

    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="A simple task cli",
        epilog="Made by PWDSerialgamer07"
    )
    # All commands : list, add, delete, mark, update

    subparsers = parser.add_subparsers(dest="command", required=True)

    # List command
    add_command_parser(
        subparsers,
        "list",
        "List tasks by status (all, ongoing, completed, and todo)",
        (["status"], {"nargs": "?", "choices": ["ongoing", "todo", "completed"],
         "help": "Filter tasks by status, or print all of them if not specified"})
    )

    # Add command
    add_command_parser(
        subparsers,
        "add",
        "Add a new task (description is required)",
        (["description"], {"help": "The description of the task"})
    )

    # Delete command
    add_command_parser(
        subparsers,
        "delete",
        "Delete a task by id",
        (["id"], {"help": "The id of the task to delete"})
    )

    # Mark command
    add_command_parser(
        subparsers,
        "mark",
        "Mark a task as completed or ongoing (args: status id)",
        (["status"], {"choices": ["completed", "ongoing",
         "todo"], "help": "The status to mark the task"}),
        (["id"], {"help": "The id of the task to mark"})
    )

    # Update command
    add_command_parser(
        subparsers,
        "update",
        "Update the description of a task (args: id description)",
        (["id"], {"help": "The id of the task to update"}),
        (["description"], {"help": "The new description of the task"})
    )

    args = parser.parse_args()
    if args.command in command_options:
        command_options[args.command](args)
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
