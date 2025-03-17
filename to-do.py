import os
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

tasks = []

def clear_screen():
    """Clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_priority(priority):
    """Ensures the entered priority is valid"""
    return priority in ["High", "Medium", "Low"]

def show_tasks():
    """Displays tasks with colors and formatting"""
    clear_screen()
    print(Fore.CYAN + "=" * 30)
    print(Fore.YELLOW + "\U0001F4CC To-Do List".center(30))
    print(Fore.CYAN + "=" * 30)

    if not tasks:
        print(Fore.RED + "\nNo tasks found.\n")
    else:
        for i, task in enumerate(tasks, 1):
            status_icon = Fore.GREEN + "🎉" if task["status"] else Fore.YELLOW + "🕒"
            priority_icon = (
                Fore.RED + "🚀" if task["priority"] == "High" else
                Fore.YELLOW + "⚡" if task["priority"] == "Medium" else
                Fore.GREEN + "🛶"
            )            
            print(f"{Fore.BLUE}{i}. {task['task']} {priority_icon} {status_icon}")

    print(Fore.CYAN + "=" * 30)

def add_task():
    """Adds a new task with validated priority"""
    task = input(Fore.GREEN + "\nEnter a new task: ").strip()
    if not task:
        print(Fore.RED + "Task cannot be empty!")
        return

    while True:
        priority = input(Fore.GREEN + "Enter priority (High, Medium, Low): ").capitalize()
        if validate_priority(priority):
            break
        print(Fore.RED + "Invalid priority! Please enter High, Medium, or Low.")

    tasks.append({"task": task, "status": False, "priority": priority})
    print(Fore.GREEN + f"Task '{task}' added successfully!")
    save_tasks()

def remove_task():
    """Removes a task based on user input"""
    show_tasks()
    try:
        index = int(input(Fore.RED + "\nEnter task number to remove: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(Fore.RED + f"Task '{removed['task']}' removed!")
            save_tasks()
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")

def complete_task():
    """Marks a task as completed"""
    show_tasks()
    try:
        index = int(input(Fore.CYAN + "\nEnter task number to complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["status"] = True
            print(Fore.GREEN + f"Task '{tasks[index]['task']}' marked as completed! 🎉")
            save_tasks()
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")

def edit_task():
    """Edits an existing task and validates priority"""
    show_tasks()
    try:
        index = int(input(Fore.CYAN + "\nEnter task number to edit: ")) - 1
        if 0 <= index < len(tasks):
            task = input(Fore.GREEN + "Enter a new task (Press Enter to keep current): ").strip()
            task = task if task else tasks[index]["task"]

            priority = input(Fore.GREEN + "Enter new priority (High, Medium, Low) or press Enter to keep current: ").capitalize()
            if priority:
                if not validate_priority(priority):
                    print(Fore.RED + "Invalid priority! Keeping the current one.")
                    priority = tasks[index]["priority"]
            else:
                priority = tasks[index]["priority"]

            tasks[index] = {"task": task, "status": tasks[index]["status"], "priority": priority}
            print(Fore.GREEN + f"Task '{task}' edited successfully!")
            save_tasks()
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")

def save_tasks():
    """Writes tasks to a text file"""
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(f"{task['task']}|{task['status']}|{task['priority']}\n")

def load_tasks():
    """Reads tasks from a text file"""
    if os.path.exists("tasks.txt"):
        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                for line in file:
                    task, status, priority = line.strip().split("|")
                    tasks.append({"task": task, "status": status == "True", "priority": priority})
            print(Fore.GREEN + f"Loaded {len(tasks)} tasks successfully!")
        except Exception as e:
            print(Fore.RED + f"Error loading tasks: {e}")

# Load tasks on startup
load_tasks()

while True:
    print(Fore.MAGENTA + "\nTo-Do List")
    print(Fore.MAGENTA + "=" * 10)
    print(Fore.CYAN + "1. View Tasks")
    print(Fore.GREEN + "2. Add Task")
    print(Fore.RED + "3. Remove Task")
    print(Fore.YELLOW + "4. Complete Task")
    print(Fore.BLUE + "5. Edit Task")
    print(Fore.WHITE + "6. Exit")
    
    choice = input(Fore.MAGENTA + "Enter your choice: ")

    if choice == "1":
        show_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        remove_task()
    elif choice == "4":
        complete_task()
    elif choice == "5":
        edit_task()
    elif choice == "6":
        print(Fore.CYAN + "Goodbye! 👋")
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter a number between 1-6.")