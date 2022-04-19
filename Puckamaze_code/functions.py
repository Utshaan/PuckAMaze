from screen import *
from itertools import product
from random import choice
from pellets import PowerPellets

def setit(number: int) -> None:
    """sets an entire set of power Pellets

    Args:
        number (int): number of pellets in every row/column
    """
    for i, j in product(range(number), repeat=2):
        PowerPellets(
            (2 * i + 1) * WIDTH // (2 * number),
            dis_level_height
            + ((2 * j + 1) * (HEIGHT - dis_level_height) // (number * 2)),
            pellet_group,
        )

def get_cell(pos: tuple) -> tuple:
    x_cell = num_row * pos[0] // WIDTH
    y_cell = (
        num_col
        * (pos[1] - dis_level_height)
        // (HEIGHT - dis_level_height)
    )
    return (2 * x_cell, 2 * y_cell)

def get_coord(x: int, y: int) -> tuple:
    absc = x * WIDTH // (2 * num_row) + WIDTH // (2 * num_row)
    oord = (
        dis_level_height
        + y * (HEIGHT - dis_level_height) // (2 * num_col)
        + (HEIGHT - dis_level_height) // (2 * num_col)
    )
    return (absc, oord)

def rand_level_maker(row_len:int = num_row, col_len:int = num_col) -> None:
    map_level = []
    temp = " "
    for _ in range(row_len - 1):
        temp += choice(shuffle_list[1:5])
    map_level.append(list(temp))
    for _ in range(col_len - 2):
        s = choice([" ", "h"])
        for _ in range(row_len - 2):
            s += choice(shuffle_list)
        s += choice(shuffle_list[:-1])
        map_level.append(list(s))
    temp = " "
    for _ in range(row_len - 1):
        temp += choice(shuffle_list[1:5])
    map_level.append(list(temp))
    map_level[1][0] = " "
    return map_level

def menu_cycle(buttons: tuple, CnCinfo: list[int, int] = [0,0]) -> int:
    keys = pg.key.get_pressed()
    down = False
    if keys[pg.K_DOWN]:
        CnCinfo[1] = 1
        buttons[CnCinfo[0]].hovering = False
        down = True
    if keys[pg.K_UP]:
        CnCinfo[1] = -1
        buttons[CnCinfo[0]].hovering = False
        down = True
    if keys[pg.K_SPACE]:
        buttons[CnCinfo[0]].pressed = True
        down = True
    if not down:
        CnCinfo[0] += CnCinfo[1]
        CnCinfo[0] = CnCinfo[0]%len(buttons)
        CnCinfo[1] = 0
        for button in buttons:
            if button.pressed:
                button.released = True
                buttons[CnCinfo[0]].selected = not buttons[CnCinfo[0]].selected
                button.pressed = False
            else:
                button.released = False
        buttons[CnCinfo[0]].hovering = True
    return CnCinfo