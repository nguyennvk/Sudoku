import customtkinter as ctk
from sudoku_color import *
from PIL import Image, ImageTk

class Button(ctk.CTkButton):
    def __init__(self, parent, clear_func):
        font = ctk.CTkFont(family="Calibri", size=40)
        super().__init__(master=parent, bg_color=BACKGROUND_COLOR, text="Start", corner_radius=9, width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                         font=font, fg_color=(BUTTON["light"]["color"], BUTTON["dark"]["color"]),
                         text_color=(BUTTON["light"]["text"], BUTTON["dark"]["text"]),
                         hover_color=(BUTTON["light"]["hover"], BUTTON["dark"]["hover"]),
                         border_color=(BUTTON["light"]["text"], BUTTON["dark"]["text"]), border_width=3,
                         command=self.clear)
        self.place(relx=0.5, rely=0.75, anchor="center")
        self.clear_func = clear_func

    def clear(self):
        self.clear_func()

class ImageButton(ctk.CTkButton):
    def __init__(self, parent, light_mode):
        self.light_mode = light_mode
        self.image = Image.open("light mode.png").resize((BUTTON_SIZE[0], BUTTON_SIZE[1]))
        self.imagetk = ImageTk.PhotoImage(self.image)
        self.image_dark = Image.open("dark mode.png").resize((BUTTON_SIZE[0], BUTTON_SIZE[1]))
        self.imagetk_dark = ImageTk.PhotoImage(self.image_dark)
        super().__init__(master=parent, image=self.imagetk, text="",
                         width=BUTTON_SIZE[0]-20, height=BUTTON_SIZE[1]-20, fg_color=BACKGROUND_COLOR, border_width=0,
                         hover=False, command=self.change)
        self.place(relx=0.5, rely=0.85, anchor="center")

    def change(self):
        if self.light_mode.get():
            self.configure(image=self.imagetk_dark)
            self.light_mode.set(False)
        else:
            self.configure(image=self.imagetk)
            self.light_mode.set(True)
