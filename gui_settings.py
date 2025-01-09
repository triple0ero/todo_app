import json
import customtkinter as ctk
from tkinter import messagebox, colorchooser

class SettingsWindow:
    SETTINGS_FILE = "./data/settings.json"

    DEFAULTS = {
        "bg_color": "white",
        "button_color": "black",
        "secondary_color": "lightgray"
    }

    def __init__(self, parent, button_color):
        self.parent = parent
        self.settings_window = ctk.CTkToplevel(parent)
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x400")

        ctk.CTkLabel(self.settings_window, text="Background Color:").pack(pady=5)
        self.bg_color_button = ctk.CTkButton(self.settings_window, text="Choose Color", command=self.choose_bg_color)
        self.bg_color_button.pack(pady=5)
    
        ctk.CTkLabel(self.settings_window, text="Button Color:").pack(pady=5)
        self.button_color_button = ctk.CTkButton(self.settings_window, text="Choose Color", command=self.choose_button_color)
        self.button_color_button.pack(pady=5)

        ctk.CTkLabel(self.settings_window, text="Secondary Color:").pack(pady=5)
        self.secondary_color_button = ctk.CTkButton(self.settings_window, text="Choose Color", command=self.choose_secondary_color)
        self.secondary_color_button.pack(pady=5)

        self.save_button = ctk.CTkButton(self.settings_window, text="Save", command=self.save_settings, fg_color=button_color, hover_color=button_color)
        self.save_button.pack(pady=10)

        self.discard_button = ctk.CTkButton(self.settings_window, text="Discard", command=self.settings_window.destroy, fg_color=button_color, hover_color=button_color)
        self.discard_button.pack(pady=5)

        self.restore_defaults_button = ctk.CTkButton(self.settings_window, text="Restore Defaults", command=self.restore_defaults, fg_color=button_color, hover_color=button_color)
        self.restore_defaults_button.pack(pady=10)

        self.load_settings()

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose Background Color")
        if color_code[1]:
            self.bg_color_button.configure(fg_color=color_code[1])

    def choose_button_color(self):
        color_code = colorchooser.askcolor(title="Choose Button Color")
        if color_code[1]:
            self.button_color_button.configure(fg_color=color_code[1])

    def choose_secondary_color(self):
        color_code = colorchooser.askcolor(title="Choose Secondary Color")
        if color_code[1]:
            self.secondary_color_button.configure(fg_color=color_code[1])

    def save_settings(self):
        bg_color = self.bg_color_button.cget("fg_color")
        button_color = self.button_color_button.cget("fg_color")
        secondary_color = self.secondary_color_button.cget("fg_color")
        
        settings = {
            "bg_color": bg_color,
            "button_color": button_color,
            "secondary_color": secondary_color
        }
        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)

        self.parent.apply_settings(settings)
        self.settings_window.destroy()

    def load_settings(self):
        try:
            with open(self.SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                self.bg_color_button.configure(fg_color=settings["bg_color"])
                self.button_color_button.configure(fg_color=settings["button_color"])
                self.secondary_color_button.configure(fg_color=settings["secondary_color"])
        except FileNotFoundError:
            pass

    def restore_defaults(self):
        self.bg_color_button.configure(fg_color=self.DEFAULTS["bg_color"])
        self.button_color_button.configure(fg_color=self.DEFAULTS["button_color"])
        self.secondary_color_button.configure(fg_color=self.DEFAULTS["secondary_color"])

        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(self.DEFAULTS, f)

        self.parent.apply_settings(self.DEFAULTS)
        self.update_button_colors()

    def update_button_colors(self):
        button_color = self.DEFAULTS["button_color"]

        for button in [self.save_button, self.discard_button, self.restore_defaults_button]:
            button.configure(fg_color=button_color, hover_color=button_color)