import customtkinter
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from Menupage import *
from Start import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.iconbitmap("Icon.ico")
        self.geometry(f"{SIZE[0]}x{SIZE[1]}+0+0")
        self.resizable(False, False)
        self.light_mode = tk.BooleanVar(value=True)

        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        Menu(self, self.light_mode)

        self.mainloop()



class Menu(ctk.CTkFrame):
    def __init__(self, parent, light_mode):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky="news")
        self.rowconfigure(0, weight=5, uniform="b")
        self.rowconfigure(1, weight=2, uniform="b")
        self.columnconfigure((0, 1, 2), weight=1, uniform="b")

        self.width, self.height = SIZE[0]*1.5, SIZE[1]*1.5
        self.menu_image = Image.open("SUDOKU_light.png").resize((int(self.width), int(self.height)))
        self.menu_imagetk = ImageTk.PhotoImage(self.menu_image)
        self.menu_image_dark = Image.open("SUDOKU_dark.png").resize((int(self.width), int(self.height)))
        self.menu_imagetk_dark = ImageTk.PhotoImage(self.menu_image_dark)

        self.canva = ctk.CTkCanvas(self, background="blue", bd=0, highlightthickness=0)
        self.canva.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="news")
        self.canva.create_image(self.width/2, self.height/2, image=self.menu_imagetk, anchor="center")

        self.light_mode = light_mode
        self.light_mode.trace("w", self.change)

        self.button = Button(self, self.clear_func)
        self.image_button = ImageButton(self, light_mode)

    def clear_func(self):
        # self.grid_forget()
        frame = ctk.CTkFrame(self, fg_color=("#e4e4e4", "#292929"))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="news")
        frame_1 = ctk.CTkFrame(self, width=GRID[0], height=4, fg_color=TEXT_COLOR, corner_radius=0, border_width=0)
        frame_1.place(relx=0.499, rely=0.113, anchor="center")
        frame_2 = ctk.CTkFrame(self, width=4, height=GRID[0]-3, fg_color=TEXT_COLOR, corner_radius=0, border_width=0)
        frame_2.place(relx=0.066, rely=0.113, anchor="n")
        frame_3 = ctk.CTkFrame(self, width=GRID[0]+1.5, height=4, fg_color=TEXT_COLOR, corner_radius=0, border_width=0)
        frame_3.place(relx=0.4999, rely=0.688, anchor="center")
        frame_4 = ctk.CTkFrame(self, width=4, height=GRID[0]-0.7, fg_color=TEXT_COLOR, corner_radius=0, border_width=0)
        frame_4.place(relx=0.933, rely=0.1097, anchor="n")

        self.start = start
        self.action = []
        self.button_dict = {}
        self.end = ctk.BooleanVar(value=False)

        font = ctk.CTkFont(family="MS Serif", size=60, weight="bold")
        ctk.CTkLabel(self, text="SUDOKU", font=font, fg_color=BACKGROUND_COLOR, text_color=TEXT_COLOR).place(relx=0.5, rely=0.055, anchor="center")


        self.count = ctk.IntVar(value=0)

        Grid(self, self.start, self.action, self.button_dict)
        Panel(self, self.start, self.action, self.button_dict, self.count, self.result)
        Eraser(self, self.start, self.action, self.button_dict)
        Timer(self, self.count)

        self.after(1000, self.a)

    def a(self):
        if not self.end.get():
            self.count.set(self.count.get()+1)
            Timer(self, self.count)
            self.after(1000, self.a)

    def result(self, s):
        self.end.set(True)
        frame = ctk.CTkFrame(self, fg_color=("#e4e4e4", "#292929"))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="news")
        ctk.CTkLabel(frame, text=f"You win!", font=("Calibri", 50)).place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(frame, text=s, font=("Calibri", 50)).place(relx=0.5, rely=0.5, anchor="center")

    def change(self, *args):
        if not self.light_mode.get():
            customtkinter.set_appearance_mode("dark")
            self.canva.delete()
            self.canva.create_image(self.width/2, self.height/2, image=self.menu_imagetk_dark, anchor="center")
        else:
            customtkinter.set_appearance_mode("light")
            self.canva.delete()
            self.canva.create_image(self.width / 2, self.height / 2, image=self.menu_imagetk, anchor="center")



App()