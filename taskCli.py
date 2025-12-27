import json
import os
import sys
from datetime import datetime

DATA_FILE = 'task.json'

def loadTask():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []
    
def saveTask(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def findTaskById(tasks, taskId):
    try:
        taskId = int(taskId)
        for task in tasks:
            if task['id'] == taskId:
                return task
        return None
    except ValueError:
        return None

def addTask(description):
    tasks = loadTask()
    nextId = tasks[-1]['id'] + 1 if tasks else 1
    currentTime = datetime.now().isoformat()

    newTask = {
        'id': nextId,
        'description': description,
        'status': 'todo',
        'createdAt': currentTime,
        'updatedAt': currentTime
    }

    tasks.append(newTask)
    saveTask(tasks)
    print(f"Task added successfully (ID: {nextId})")

def listTask(statusFilter=None):
    tasks = loadTask()

    if not tasks:
        print("No tasks found.")
        return
    
    statusFilter = statusFilter.lower() if statusFilter else None

    if statusFilter:
        if statusFilter not in ['todo', 'in-progress', 'done', 'inProgress']:
             print(f"Error: Invalid status filter '{statusFilter}'. Use todo, in-progress, or done.")
             return
        
        # Penanganan in-progress/inProgress
        if statusFilter == 'in-progress':
            statusFilter = 'inProgress' 

        filteredTask = [t for t in tasks if t['status'] == statusFilter]
    else:
        filteredTask = tasks
    
    if not filteredTask:
        print(f"No tasks found with status: {statusFilter}")
        return
    
    print ("\n--- Task List ---")
    for task in filteredTask:
        statusDisplay = {
            'todo': '[ ] TODO',
            'inProgress': '[>] IN-PROGRESS',
            'done': '[X] DONE'
        }.get(task['status'], '[?] UNKNOWN')

        print(f"ID: {task['id']} | Status: {statusDisplay} | Description: {task['description']}")
    print("-----------------\n")

def updateTaskDescription(taskId, newDescription):
    tasks = loadTask()
    task = findTaskById(tasks, taskId)

    if task:
        task['description'] = newDescription
        task['updatedAt'] = datetime.now().isoformat()
        saveTask(tasks) 
        print(f"Task ID {taskId} updated successfully")
    else:
        print(f"Error: Task with ID {taskId} not found")

def setTaskStatus(taskId, newStatus):
    tasks = loadTask()
    task = findTaskById(tasks, taskId)

    if task:
        if newStatus in ['todo', 'inProgress', 'done']:
            task['status'] = newStatus
            task['updatedAt'] = datetime.now().isoformat()
            saveTask(tasks)
            print(f"Task ID {taskId} marked as {newStatus.upper()}.")
        else:
            print(f"Error: Invalid status '{newStatus}'.")
    else:
        print(f"Error: Task with ID {taskId} not found")

def markInProgress(taskId):
    setTaskStatus(taskId, 'inProgress')

def markDone(taskId):
    setTaskStatus(taskId, 'done')
    
def deleteTask(taskId):
    tasks = loadTask()
    initial_length = len(tasks)
    
    try:
        task_id_int = int(taskId)
    except ValueError:
        print(f"Error: Invalid ID format '{taskId}'.")
        return

    tasks = [t for t in tasks if t['id'] != task_id_int]

    if len(tasks) < initial_length:
        saveTask(tasks)
        print(f"Task ID {taskId} deleted successfully.")
    else:
        print(f"Error: Task with ID {taskId} not found.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py <action> [arguments]")
        print("Available actions: add, list, update, delete, mark-in-progress, mark-done")
        return

    action = sys.argv[1].lower() 
    
    if action == 'add':
        if len(sys.argv) < 3:
            print("Usage: python task_cli.py add \"<description>\"")
            return
        description = sys.argv[2]
        addTask(description)

    elif action == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        listTask(status)

    elif action == 'update':
        if len(sys.argv) < 4:
            print("Usage: python task_cli.py update <id> \"<new_description>\"")
            return
        task_id = sys.argv[2]
        new_description = sys.argv[3]
        updateTaskDescription(task_id, new_description)

    elif action == 'delete':
        if len(sys.argv) < 3:
            print("Usage: python task_cli.py delete <id>")
            return
        deleteTask(sys.argv[2])
        
    elif action == 'mark-in-progress':
        if len(sys.argv) < 3:
            print("Usage: python task_cli.py mark-in-progress <id>")
            return
        markInProgress(sys.argv[2])

    elif action == 'mark-done':
        if len(sys.argv) < 3:
            print("Usage: python task_cli.py mark-done <id>")
            return
        markDone(sys.argv[2])

    else:
        print(f"Error: Unknown action '{action}'")

if __name__ == '__main__':
    main()