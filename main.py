import customtkinter as ctk
from PIL import Image, ImageTk
from gui import TodoApp

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = TodoApp()

    icon_image = Image.open("./data/icon.png")
    icon_photo = ImageTk.PhotoImage(icon_image)

    app.iconphoto(False, icon_photo)
    app.mainloop()