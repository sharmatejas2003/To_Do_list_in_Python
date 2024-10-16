import tkinter as tk
from tkinter import messagebox
import json
import os

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.filename = 'tasks.json'
        self.tasks = self.load_tasks()

        self.task_var = tk.StringVar()

        # Entry for new tasks
        self.task_entry = tk.Entry(master, textvariable=self.task_var, width=50)
        self.task_entry.pack(pady=10)

        # Add task button
        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        # Listbox for displaying tasks
        self.task_listbox = tk.Listbox(master, width=50, height=10)
        self.task_listbox.pack(pady=10)

        # Mark complete button
        self.mark_complete_button = tk.Button(master, text="Mark Complete", command=self.mark_complete)
        self.mark_complete_button.pack(pady=5)

        # Delete task button
        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        # Load existing tasks into the listbox
        self.load_tasks_to_listbox()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self):
        """Add a new task."""
        task = self.task_var.get()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.save_tasks()
            self.load_tasks_to_listbox()
            self.task_var.set("")  # Clear the entry
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def mark_complete(self):
        """Mark the selected task as complete."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]['completed'] = True
            self.save_tasks()
            self.load_tasks_to_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as complete.")

    def delete_task(self):
        """Delete the selected task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.save_tasks()
            self.load_tasks_to_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def load_tasks_to_listbox(self):
        """Load tasks into the listbox for display."""
        self.task_listbox.delete(0, tk.END)  # Clear the listbox
        for task in self.tasks:
            status = "✓" if task['completed'] else "✗"
            self.task_listbox.insert(tk.END, f"{task['task']} [{status}]")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
