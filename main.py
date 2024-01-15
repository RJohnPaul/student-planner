import os
import json
from datetime import datetime, timedelta

class StudentPlanner:
    def __init__(self, data_file='student_data.json'):
        self.data_file = data_file
        self.tasks = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        else:
            return []

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, title, deadline_str, description='', priority='Low'):
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
        task = {'title': title, 'deadline': deadline_str, 'description': description, 'priority': priority}
        self.tasks.append(task)
        self.save_data()

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            print("Tasks:")
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task['title']} - Deadline: {task['deadline']} - Priority: {task['priority']} - Description: {task['description']}")

    def remove_task(self, index):
        if 1 <= index <= len(self.tasks):
            removed_task = self.tasks.pop(index - 1)
            print(f"Removed task: {removed_task['title']} - Deadline: {removed_task['deadline']}")
            self.save_data()
        else:
            print("Invalid task index.")

    def upcoming_tasks(self, days=7):
        now = datetime.now()
        deadline_limit = now + timedelta(days=days)
        upcoming = [task for task in self.tasks if datetime.strptime(task['deadline'], '%Y-%m-%d %H:%M') <= deadline_limit]

        if not upcoming:
            print(f"No upcoming tasks in the next {days} days.")
        else:
            print(f"Upcoming tasks in the next {days} days:")
            for task in upcoming:
                print(f"{task['title']} - Deadline: {task['deadline']} - Priority: {task['priority']} - Description: {task['description']}")

    def overdue_tasks(self):
        now = datetime.now()
        overdue = [task for task in self.tasks if datetime.strptime(task['deadline'], '%Y-%m-%d %H:%M') < now]

        if not overdue:
            print("No overdue tasks.")
        else:
            print("Overdue tasks:")
            for task in overdue:
                print(f"{task['title']} - Deadline: {task['deadline']} - Priority: {task['priority']} - Description: {task['description']}")

    def edit_task(self, index, title=None, deadline=None, description=None, priority=None):
        if 1 <= index <= len(self.tasks):
            task = self.tasks[index - 1]

            if title:
                task['title'] = title
            if deadline:
                task['deadline'] = deadline
            if description:
                task['description'] = description
            if priority:
                task['priority'] = priority

            print(f"Task edited: {task['title']} - Deadline: {task['deadline']} - Priority: {task['priority']} - Description: {task['description']}")
            self.save_data()
        else:
            print("Invalid task index.")

    def prioritize_tasks(self):
        self.tasks.sort(key=lambda x: (x['priority'], datetime.strptime(x['deadline'], '%Y-%m-%d %H:%M')))
        print("Tasks prioritized.")

    def search_tasks(self, keyword):
        matches = [task for task in self.tasks if keyword.lower() in task['title'].lower() or (task['description'] and keyword.lower() in task['description'].lower())]
        if matches:
            print(f"Tasks containing '{keyword}':")
            for match in matches:
                print(f"{match['title']} - Deadline: {match['deadline']} - Priority: {match['priority']} - Description: {match['description']}")
        else:
            print(f"No tasks found containing '{keyword}'.")

if __name__ == "__main__":
    planner = StudentPlanner()

    while True:
        print("\nStudent Planner Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Remove Task")
        print("4. Upcoming Tasks")
        print("5. Overdue Tasks")
        print("6. Edit Task")
        print("7. Prioritize Tasks")
        print("8. Search Tasks")
        print("9. Save and Exit")
        print("10. Exit without Saving")

        choice = input("Enter your choice (1-10): ")

        if choice == '1':
            title = input("Enter task title: ")
            deadline = input("Enter task deadline (format: YYYY-MM-DD HH:MM): ")
            description = input("Enter task description (optional): ")
            priority = input("Enter task priority (Low/Medium/High, default is Low): ").capitalize()
            priority = priority if priority in ['Low', 'Medium', 'High'] else 'Low'
            planner.add_task(title, deadline, description, priority)
        elif choice == '2':
            planner.list_tasks()
        elif choice == '3':
            index = int(input("Enter the index of the task to remove: "))
            planner.remove_task(index)
        elif choice == '4':
            days = int(input("Enter the number of days to look ahead: "))
            planner.upcoming_tasks(days)
        elif choice == '5':
            planner.overdue_tasks()
        elif choice == '6':
            index = int(input("Enter the index of the task to edit: "))
            title = input("Enter new task title (press Enter to keep the current title): ")
            deadline = input("Enter new task deadline (press Enter to keep the current deadline): ")
            description = input("Enter new task description (press Enter to keep the current description): ")
            priority = input("Enter new task priority (Low/Medium/High, press Enter to keep the current priority): ").capitalize()
            priority = priority if priority in ['Low', 'Medium', 'High'] else None
            planner.edit_task(index, title, deadline, description, priority)
        elif choice == '7':
            planner.prioritize_tasks()
        elif choice == '8':
            keyword = input("Enter a keyword to search for in tasks: ")
            planner.search_tasks(keyword)
        elif choice == '9':
            planner.save_data()
            print("Data saved. Exiting Student Planner.")
            break
        elif choice == '10':
            print("Exiting Student Planner without saving.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")
