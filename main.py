import os
import time
import json
import argparse


def json_check():  # checks if the task file exists
    if os.path.exists('tasks.json'):
        pass
    else:
        with open('tasks.json', 'w') as tasks:
            tasks.write('{}')


def read_json_content():
    json_check()
    with open('tasks.json', 'r') as tasks:
        return tasks.read()


def list_tasks(args=None):
    if args.status:
        print(f"Listing all tasks with status {args.status}")
    else:
        print("Listing all tasks")


def add_task(args):
    print(f"Adding task {args.description}")


def delete_task(args):
    print(f"deleting task {args.id}")


def mark(args):
    print(f"Marking task {args.id} as {args.status}")


def update(args):
    print(f"Updating task {args.id} to {args.description}")


def add_command_parser(subparsers, command, help_text, *args):
    """Helper function to add a subcommand parser."""
    parser = subparsers.add_parser(command, help=help_text)
    for arg in args:
        parser.add_argument(*arg[0], **arg[1])
    return parser


def main():
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
