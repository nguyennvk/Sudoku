import random
import time
from random import randint
from sudoku_color import num_empty


def check_wrong(d: dict, row, col) -> set:

    set_num = set()
    for x in range(9):
        if d[(row, x)] != 0:
            set_num.add(d[row, x])
    for x in range(9):
        if d[(x, col)] != 0:
            set_num.add(d[x, col])
    base_col = (col // 3) * 3
    base_row = (row // 3) * 3
    for x in range(3):
        for i in range(3):
            if d[(base_row + x, base_col + i)] != 0:
                set_num.add(d[(base_row + x, base_col + i)])
    return set_num


def _helper_check_wrong(d: dict, row: int, col: int) -> list:
    s = check_wrong(d, row, col)
    l = []
    for x in range(1, 10):
        if x not in s:
            l.append(x)
    return l


def inti_grid() -> dict:
    d = {}
    for x in range(9):
        for i in range(9):
            d[(x, i)] = 0
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(l)
    for x in range(3):
        for i in range(3):
            d[(x, i)] = l[x*3+i]
    for x in range(3, 6):
        for i in range(3, 6):
            a = _helper_check_wrong(d, i, x)
            random.shuffle(a)
            d[(i, x)] = a[0]
    for x in range(6, 9):
        for i in range(6, 9):
            a = _helper_check_wrong(d, i, x)
            random.shuffle(a)
            d[(i, x)] = a[0]
    back_track(d, 0, 3)
    return d


def back_track(d, row, col):

    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if d[(row, col)] > 0:
        return back_track(d, row, col + 1)

    for num in _helper_check_wrong(d, row, col):
        d[(row, col)] = num
        if back_track(d, row, col+1):
            return True
        d[(row, col)] = 0
    return False

def remove(d, n):
    for x in range(n):
        row, col = randint(0, 8), randint(0, 8)
        while d[(row, col)] == 0:
            row, col = randint(0, 8), randint(0, 8)
        d[(row, col)] = 0





def print_table(d: dict) -> str:
    sudoku_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for x in d:
        sudoku_board[x[0]][x[1]] = d[x]
    s = ""
    for x in sudoku_board:
        s += f'{x}\n'
    return s


def input_move(d: dict, l, row, col, num) -> dict:
    if 10 > row > 0 and 10 > col > 0 and 10 > num > 0:
        if (row-1, col-1) in l:
            print("CANNOT!!!")
        elif num in check_wrong(d, row-1, col-1):
            print("WRONG!!!!")
            d[(row - 1, col - 1)] = num
        else:
            d[(row - 1, col - 1)] = num
    return d

def check_win(d: dict):
    for x in range(9):
        for i in range(9):
            if len(check_wrong(d, x, i)) != 9:
                return False
    return True


def convert_time(n):
    sec = n%60
    min = n//60
    hour = min//60

    sec_str = str(sec)
    min_str = str(min)
    hour_str = str(hour)

    if sec < 10:
        sec_str = f"0{sec}"
    if min < 10:
        min_str = f"0{min}"
    if hour < 10:
        hour_str = f"0{hour}"
    return f"{hour_str}:{min_str}:{sec_str}"


number_of_empty = num_empty
start = inti_grid()
d = start
game = True
table = print_table(d)
