# Task-CLI

A basic task cli made for a roadmap.sh project (https://roadmap.sh/projects/task-tracker)

## Setup:

- Clone repository to a folder of your choice.
- Open a terminal and cd into said folder.
- Run "pip install ."
- You can now run "task-cli -h" anywhere on your pc.

## Commands:

- `task-cli -h`
Shows the help screen:
```
usage: task-cli [-h] {list,add,delete,mark,update} ...

A simple task cli

positional arguments:
  {list,add,delete,mark,update}
    list                List tasks by status (all, ongoing, completed, and todo)
    add                 Add a new task (description is required)
    delete              Delete a task by id
    mark                Mark a task as completed or ongoing (args: status id)
    update              Update the description of a task (args: id description)

options:
  -h, --help            show this help message and exit

Made by PWDSerialgamer07
```
- `task-cli list [status}`

Lists all tasks or filters tasks by status, displaying their ID, description, status, dates of creation and modification.

Choices: "ongoing", "completed, "todo" and nothing.

- `task-cli add [description]`

Adds a new task with the specified description. Description required.

- `task-cli delete [ID]`

Deletes a task by its ID. ID required.

- `task-cli mark [status] [ID]`

Marks a task as completed, ongoing, or todo using their ID.

- `task-cli update [ID] [Description]`

Updates the description of a task.
