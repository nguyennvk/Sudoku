from sudoku import *
import customtkinter as ctk
from sudoku_color import *
from PIL import Image


class Grid(ctk.CTkFrame):
    def __init__(self, parent, start, action, dict):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR, width=GRID[0], height=GRID[1], corner_radius=0)


        self.place(relx=0.5, rely=0.4, anchor="center")
        self.columnconfigure(list(range(9)), weight=1, uniform="c")
        self.rowconfigure(list(range(9)), weight=1, uniform="c")
        self.action = action


        self.play_grid = start
        self.button_dict = dict
        for x in range(9):
            for i in range(9):
                if self.play_grid[(x, i)] != 0:
                    self.button_dict[(x, i)] = FixedButton(self, self.play_grid[(x, i)], x, i)
                else:
                    self.button_dict[(x, i)] = PlayButton(self, " ", x, i, self.action, self.button_dict, self.func)

        for x in range(1, 4):
            ctk.CTkFrame(self, width=2, height=GRID[0], fg_color=TEXT_COLOR, corner_radius=0, border_width=0).\
                place(relx=x/3, rely=0, anchor="n")

        for x in range(1, 4):
            ctk.CTkFrame(self, width=GRID[0], height=2, fg_color=TEXT_COLOR, corner_radius=0, border_width=0).\
                place(rely=x/3, relx=0, anchor="w")

    def func(self, r, c, t=None):

        if t is not None:
            for x in range(9):
                self.button_dict[(x, t[1])].configure(fg_color=(TEXT_COLOR[1], TEXT_COLOR[0]))
            for x in range(9):
                self.button_dict[(t[0], x)].configure(fg_color=(TEXT_COLOR[1], TEXT_COLOR[0]))

        for x in range(9):
            self.button_dict[(r, x)].configure(fg_color=OTHER)
        for x in range(9):
            self.button_dict[(x, c)].configure(fg_color=OTHER)

        self.button_dict[(r, c)].configure(fg_color=NUMBER_BUTTON_HOVER)





class Panel(ctk.CTkFrame):
    def __init__(self, parent, start, action, dict, sec, end):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR, corner_radius=0)
        self.place(relx=0.5, rely=0.75, anchor="center", relwidth=0.99, relheight=0.072)
        self.play_grid = start
        self.action = action
        self.dict = {}
        self.button_dict = dict
        for x in range(1, 10):
            self.dict[x] = InputButton(self, x, self.play_grid, self.action, self.button_dict, sec, end)

class Eraser(ctk.CTkButton):
    def __init__(self, parent, start, action, dict):
        self.play_grid = start
        self.action = action
        self.button_dict = dict
        eraser_dark = Image.open("eraser_dark.png").resize((ERASER_SIZE[0]*2, ERASER_SIZE[1]*2))
        eraser_light = Image.open("eraser_light.png").resize((ERASER_SIZE[0]*2, ERASER_SIZE[1]*2))
        eraser_image = ctk.CTkImage(light_image=eraser_light, dark_image=eraser_dark)
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR, corner_radius=4, text="",
                         image=eraser_image, width=ERASER_SIZE[0], height=ERASER_SIZE[1], border_width=0,
                         bg_color=BACKGROUND_COLOR, hover_color=NUMBER_BUTTON_HOVER, command=self.erase)
        self.place(relx=0.5, rely=0.84, anchor="center")

    def erase(self):
        if self.action != []:
            self.play_grid[self.action[-1]] = 0
            self.button_dict[self.action[-1]].configure(text=" ")



class InputButton(ctk.CTkButton):
    def __init__(self, parent, number, start, action, dict, sec, end):
        font = ctk.CTkFont(family="Calibri", size=50)
        super().__init__(master=parent, text=number, width=41, fg_color=BACKGROUND_COLOR, text_color=TEXT_COLOR,
                         font=font, hover_color=NUMBER_BUTTON_HOVER, command=self.input)
        self.pack(side="left", expand=True, fill="both", padx=1)
        self.play_ground = start
        self.action = action
        self.number = number
        self.button_dict = dict
        self.end = end
        self.sec = sec

    def input(self):
        if self.action != []:
            self.play_ground[self.action[-1]] = self.number
            self.button_dict[self.action[-1]].configure(text=self.number)
            self.button_dict[self.action[-1]].configure(text_color=TEXT_COLOR)
            if check_win(self.play_ground):
                self.end(convert_time(self.sec.get()))
            for x in range(9):
                if self.play_ground[(x, self.action[-1][1])] == self.number and x != self.action[-1][0]:
                    self.button_dict[self.action[-1]].configure(text_color="red")
            for x in range(9):
                if self.play_ground[(self.action[-1][0], x)] == self.number and x != self.action[-1][1]:
                    self.button_dict[self.action[-1]].configure(text_color="red")

            base_col = (self.action[-1][1] // 3) * 3
            base_row = (self.action[-1][0] // 3) * 3
            for x in range(3):
                for i in range(3):
                    if self.play_ground[(base_row+x, base_col+i)] == self.number and (base_row+x, base_col+i) != self.action[-1]:
                        self.button_dict[self.action[-1]].configure(text_color="red")



class FixedButton(ctk.CTkButton):
    def __init__(self, parent, number, row, column):
        font = ctk.CTkFont(family="Calibri", size=27)
        super().__init__(master=parent, text=number, border_width=0.3, border_color=TEXT_COLOR,
                         fg_color=(TEXT_COLOR[1], TEXT_COLOR[0]), width=GRID[0]//9, height=GRID[1]//9-2, corner_radius=0,
                         text_color=TEXT_COLOR, font=font, state="disable")
        self.grid(row=row, column=column, sticky="news")

class PlayButton(ctk.CTkButton):
    def __init__(self, parent, number, row, column, action, dict, func):
        font = ctk.CTkFont(family="Calibri", size=27)
        self.func = func
        self.row = row
        self.column = column
        self.action = action
        self.button_dict = dict
        super().__init__(master=parent, text=number, border_width=0.3, border_color=TEXT_COLOR,
                         fg_color=(TEXT_COLOR[1], TEXT_COLOR[0]), width=GRID[0]//9, height=GRID[1]//9-2, corner_radius=0,
                         text_color=TEXT_COLOR, font=font, hover_color=NUMBER_BUTTON_HOVER, command=self.click)
        self.grid(row=row, column=column, sticky="news")

    def click(self):
        if len(self.action) == 0:
            self.func(self.row, self.column)
            self.action.append((self.row, self.column))
        else:
            self.func(self.row, self.column, self.action[-1])
            self.action.append((self.row, self.column))

class Timer(ctk.CTkLabel):
    def __init__(self, parent, sec):
        font = ctk.CTkFont(family="Calibri", size=50)
        text = convert_time(sec.get())
        super().__init__(master=parent, text=text, font=font,
                         fg_color=BACKGROUND_COLOR)
        self.place(relx=0.5, rely=0.94, anchor="center")
