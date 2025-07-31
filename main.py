import json
import os

# --- ANSI color codes definition ---
GREEN = "\033[32m"   # Green color
RED = "\033[31m"     # Red color
YELLOW = "\033[33m"  # Yellow color
RESET = "\033[0m"    # Reset color to default

TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, title, done=False):
        self.title = title
        self.done = done

    def mark_done(self):
        self.done = True

    def mark_undone(self):
        self.done = False

    def edit_title(self, new_title):
        self.title = new_title

    def __str__(self):
        status = f"{GREEN}✔{RESET}" if self.done else f"{RED}✗{RESET}"
        return f"{self.title} {status}"
    
    def to_dict(self):
        return {"title": self.title, "done": self.done}

class ToDoList:
    def __init__(self, filename):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content:
                        self.tasks = []
                        return
                    tasks_data = json.loads(content)
                    self.tasks = [Task(t['title'], t['done']) for t in tasks_data]
            except (json.JSONDecodeError, KeyError):
                print(f"{YELLOW}⚠️ File {self.filename} is corrupted or empty. A new list will be created.{RESET}")
                self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            tasks_to_save = [task.to_dict() for task in self.tasks]
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=4)

    def show_tasks(self):
        print(f"\n{GREEN}────── To-Do List ──────{RESET}")
        if not self.tasks:
            print("The to-do list is empty!")
        else:
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task}")
        print(f"{GREEN}────────────────────────{RESET}")

    def add_task(self, title):
        if title.strip():
            self.tasks.append(Task(title))
            self.save_tasks()
            print(f"✅ Task '{title}' was successfully added and saved.")
        else:
            print(f"{RED}❌ Task title cannot be empty!{RESET}")
            
    def edit_task(self, task_number, new_title):
        if not (1 <= task_number <= len(self.tasks)):
            print(f"{YELLOW}⚠️ Number {task_number} is invalid for editing!{RESET}")
            return
        if not new_title.strip():
            print(f"{RED}❌ New title cannot be empty!{RESET}")
            return
        old_title = self.tasks[task_number - 1].title
        self.tasks[task_number - 1].edit_title(new_title.strip())
        self.save_tasks()
        print(f"✅ Task '{old_title}' was changed to '{new_title.strip()}' and saved.")

    def mark_tasks_done(self, numbers):
        changed = False
        for num in numbers:
            if 1 <= num <= len(self.tasks):
                if not self.tasks[num - 1].done:
                    self.tasks[num - 1].mark_done()
                    changed = True
            else:
                print(f"{YELLOW}⚠️ Number {num} is invalid!{RESET}")
        if changed:
            self.save_tasks()
            print("✅ Tasks status changed to 'done' and saved.")

    def mark_tasks_undone(self, numbers):
        changed = False
        for num in numbers:
            if 1 <= num <= len(self.tasks):
                if self.tasks[num - 1].done:
                    self.tasks[num - 1].mark_undone()
                    changed = True
            else:
                print(f"{YELLOW}⚠️ Number {num} is invalid!{RESET}")
        if changed:
            self.save_tasks()
            print("✅ Tasks status changed to 'not done' and saved.")

    def delete_tasks(self, numbers):
        sorted_numbers = sorted(numbers, reverse=True)
        deleted_count = 0
        for num in sorted_numbers:
            if 1 <= num <= len(self.tasks):
                deleted_task_title = self.tasks[num - 1].title
                del self.tasks[num - 1]
                print(f"🗑️ Task '{deleted_task_title}' was successfully deleted.")
                deleted_count += 1
            else:
                print(f"{YELLOW}⚠️ Number {num} is invalid for deletion!{RESET}")
        if deleted_count > 0:
            self.save_tasks()
            print("✅ The to-do list was updated and saved.")

def main():
    todo = ToDoList(TASKS_FILE)

    while True:
        todo.show_tasks()
        
        # Changed: only the main question is green
        print(f"\n{GREEN}What would you like to do?{RESET}")
        # Menu options are displayed in the default color
        print("1. Add a new task")
        print("2. Edit a task")
        print("3. Mark tasks as done")
        print("4. Mark tasks as not done")
        print("5. Delete a task")
        print("6. Exit the program")

        prompt = f"\n{GREEN}Enter your choice (1 to 6): {RESET}"
        choice = input(prompt)

        if choice == '1':
            new_task_title = input("\nEnter the title for the new task: ")
            todo.add_task(new_task_title)
        elif choice == '2':
            if not todo.tasks:
                print("\nThere are no tasks to edit yet!")
                continue
            try:
                task_num_str = input("\nEnter the number of the task you want to edit: ")
                task_num = int(task_num_str)
                if 1 <= task_num <= len(todo.tasks):
                    print(f"Current title: {todo.tasks[task_num - 1].title}")
                    new_title = input("Enter the new title: ")
                    todo.edit_task(task_num, new_title)
                else:
                    print(f"{YELLOW}⚠️ Number {task_num} is invalid!{RESET}")
            except ValueError:
                print(f"{RED}❌ Invalid input! Please enter only an integer.{RESET}")
        elif choice == '3':
            if not todo.tasks:
                print("\nThere are no tasks to mark as done yet!")
                continue
            done_list = input("\nWhich tasks have you completed? Enter the numbers separated by a comma: ")
            try:
                done_numbers = [int(num.strip()) for num in done_list.split(",") if num.strip()]
                todo.mark_tasks_done(done_numbers)
            except ValueError:
                print(f"{RED}❌ Invalid input! Please enter only numbers and commas.{RESET}")
        elif choice == '4':
            if not todo.tasks:
                print("\nThere are no tasks to change the status of yet!")
                continue
            undone_list = input("\nWhich tasks should I mark as 'not done'? Enter the numbers separated by a comma: ")
            try:
                undone_numbers = [int(num.strip()) for num in undone_list.split(",") if num.strip()]
                todo.mark_tasks_undone(undone_numbers)
            except ValueError:
                print(f"{RED}❌ Invalid input! Please enter only numbers and commas.{RESET}")
        elif choice == '5':
            if not todo.tasks:
                print("\nThere are no tasks to delete yet!")
                continue
            delete_list = input("\nWhich tasks do you want to delete? Enter the numbers separated by a comma: ")
            try:
                delete_numbers = [int(num.strip()) for num in delete_list.split(",") if num.strip()]
                todo.delete_tasks(delete_numbers)
            except ValueError:
                print(f"{RED}❌ Invalid input! Please enter only numbers and commas.{RESET}")
        elif choice == '6':
            print("\nGoodbye!")
            break
        else:
            print(f"\n{RED}❌ Invalid choice! Please select an option from 1 to 6.{RESET}")

if __name__ == "__main__":
    main()