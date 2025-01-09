import os
import json

import customtkinter as ctk
from CTkListbox import CTkListbox
from tkinter import messagebox

from gui_settings import SettingsWindow
from todo import TodoList

class TodoApp(ctk.CTk):
    SETTINGS_FILE = "data/settings.json"

    def __init__(self):
        super().__init__()
        self.title("To-Do List Application")
        self.geometry("400x500")

        self.todo_list = TodoList()
        self.current_layout = "side_by_side"
        self.create_widgets()
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    self.apply_settings(settings)
            except json.JSONDecodeError:
                print("Error decoding JSON. Using default settings.")

    def apply_settings(self, settings):
        bg_color = settings.get("bg_color", "white")
        secondary_color = settings.get("secondary_color", "lightgray")
        button_color = settings.get("button_color", "lightblue")

        self.configure(fg_color=bg_color)
        self.task_frame.configure(bg_color=bg_color, fg_color=secondary_color)
        self.add_task_button.configure(fg_color=button_color, hover_color=button_color)
        self.delete_task_button.configure(fg_color=button_color, hover_color=button_color)
        self.settings_button.configure(fg_color=button_color, hover_color=button_color)
        self.tasks_listbox.configure(fg_color=secondary_color)

    def create_widgets(self):
        self.task_frame = ctk.CTkFrame(self)
        self.task_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.task_entry = ctk.CTkEntry(self.task_frame, placeholder_text="Task Title", width=300)
        self.task_entry.pack(pady=10)

        self.description_entry = ctk.CTkEntry(self.task_frame, placeholder_text="Task Description", width=300)
        self.description_entry.pack(pady=10)

        self.add_task_button = ctk.CTkButton(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        self.tasks_listbox = CTkListbox(self.task_frame, width=270, height=150)
        self.tasks_listbox.pack(pady=10)
        self.update_tasks_listbox()

        self.delete_task_button = ctk.CTkButton(self.task_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(self.task_frame, text="⚙️", command=self.open_settings, width=30)
        self.settings_button.pack(side=ctk.RIGHT, padx=(0, 30))

    def add_task(self):
        title = self.task_entry.get().strip()
        description = self.description_entry.get().strip()
        if self.validate_task(title, description):
            self.todo_list.add(title, description)
            self.update_tasks_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "You must enter a valid title and description.")

    def validate_task(self, title, description):
        return bool(title) and bool(description)

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if isinstance(selected_task_index, int):
            self.todo_list.remove(selected_task_index)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, ctk.END)
        for title, description in self.todo_list.get_tasks():
            self.tasks_listbox.insert(ctk.END, f"{title}: {description}")

    def clear_entries(self):
        self.task_entry.delete(0, ctk.END)
        self.description_entry.delete(0, ctk.END)

    def open_settings(self):
        button_color = self.add_task_button.cget("fg_color")
        settings_window = SettingsWindow(self, button_color)