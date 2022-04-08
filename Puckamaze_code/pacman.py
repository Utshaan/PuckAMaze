import pygame as pg
from itertools import product
import os
from time import sleep, time
import random
from pathfinding.core.grid import Grid
from buttons import Button, SettingsButton
from pathfinding.finder.a_star import AStarFinder
from math import log10
from screen import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
        temp += random.choice(shuffle_list[1:5])
    map_level.append(list(temp))
    for _ in range(col_len - 2):
        s = random.choice([" ", "h"])
        for _ in range(row_len - 2):
            s += random.choice(shuffle_list)
        s += random.choice(shuffle_list[:-1])
        map_level.append(list(s))
    temp = " "
    for _ in range(row_len - 1):
        temp += random.choice(shuffle_list[1:5])
    map_level.append(list(temp))
    map_level[1][0] = " "
    return map_level

def menu_cycle(buttons: tuple, CnCinfo: list[int, int] = [0,0]) -> int:
    keys = pg.key.get_pressed()
    down = False
    if keys[pg.K_DOWN]:
        # sleep(0.2)
        CnCinfo[1] = 1
        buttons[CnCinfo[0]].hovering = False
        down = True
    if keys[pg.K_UP]:
        # sleep(0.2)
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


class Pacman(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pg.Surface, *groups, score=0) -> None:
        """this is the summary

        Args:
            x (int): x coordinate
            y (int): y coordinate
            image (image): Image
            *groups: Groups
            score: last attained score, if any
        """
        super().__init__(*groups)
        self.to_animate = True
        self.current_image = 0
        self.score = score
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.animating_tuple = (self.image, pac_close)
        self.limit = (0, 0, SWIDTH, SHEIGHT)
        self.direction = pg.math.Vector2()
        self.temp_switch = False

    def move_direction(self, direction) -> None:
        self.rect.x += 20*direction[0]
        self.rect.y += 20* direction[1]

    def update(self, scene: str) -> None:
        """Updating the object

        Args:
            pos (tuple): (abcissa,ordinate)
            scene (str): GameState.scene
        """
        self.control()
        if scene == "initialisation" or scene == 'initialisation_2':
            self.animefy((pacman_init_image, pacman_init_close))
        elif scene == "level 1" or scene == 'start_menu':
            if self.temp_switch:
                self.temp_switch = False
                self.condition(
                    (WIDTH, dis_level_height, SWIDTH, SHEIGHT + 2 * self.rect.height)
                )
                self.rect.topleft = (WIDTH + 3, dis_level_height)
            self.animefy(self.animating_tuple, 0.05)
        elif scene == 'start_menu':
            self.animefy(self.animating_tuple, 0.05)

    def animefy(self, images, speed=0.2) -> None:
        """Handles all animations of the objects

        Args:
            image (list): The list of images to animate through
            scene (str): GameState.state
        """
        self.sprites = images
        if self.to_animate:
            self.current_image += speed
            if self.current_image >= len(self.sprites):
                self.current_image = 0
            self.image = self.sprites[int(self.current_image)]

    def get_score(self, group) -> None:
        """Checks if the object has collided with any other object and increments the score by one.

        Args:
            group (group): The group to check collision with
        """
        if pg.sprite.spritecollide(self, group, True):
            self.score += 30

    def wall_collide(self, group) -> None:
        """check collision with walls in particular

        Args:
            group (group): Gamestate.state
        """
        if pg.sprite.spritecollide(self, group, False):
            for sprite in group:
                if (
                    self.direction.x < 0
                    and abs(sprite.rect.right - self.rect.left) <= 5
                ):
                    self.rect.left = sprite.rect.right
                if (
                    self.direction.x > 0
                    and abs(sprite.rect.left - self.rect.right) <= 5
                ):
                    self.rect.right = sprite.rect.left
                if (
                    self.direction.y < 0
                    and abs(sprite.rect.bottom - self.rect.top) <= 5
                ):
                    self.rect.top = sprite.rect.bottom
                if (
                    self.direction.y > 0
                    and abs(sprite.rect.top - self.rect.bottom) <= 5
                ):
                    self.rect.bottom = sprite.rect.top

    def ghost_collide(self) -> None:
        return pg.sprite.groupcollide(pacman_group, ghosts_group, False, False, collided=pg.sprite.collide_rect_ratio(0.8))

    def control(self) -> None:
        """checks for all controls. needs no inputs"""
        self.direction.x, self.direction.y = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction.x += -1
            self.animating_tuple = (pacman_left, pac_close)
            if self.rect.x - 5 > self.limit[0]:
                self.rect.x += -5
        if keys[pg.K_s]:
            self.direction.y += 1
            self.animating_tuple = (pacman_down, pac_close_R)
            if self.rect.y + 5 < self.limit[3] - self.rect.h:
                self.rect.y += 5
        if keys[pg.K_d]:
            self.direction.x += 1
            self.animating_tuple = (pacman_right, pac_close_R)
            if self.rect.x + 5 < self.limit[2] - self.rect.w:
                self.rect.x += 5
        if keys[pg.K_w]:
            self.direction.y += -1
            self.animating_tuple = (pacman_up, pac_close)
            if self.rect.y - 5 > self.limit[1]:
                self.rect.y += -5

    def condition(self, rect_coords: tuple) -> None:
        """Confines object in a certain section

        Args:
            rect_coords (tuple) : (X1,Y1,X2,Y2)
        """
        self.limit = rect_coords


class Ghosts(pg.sprite.Sprite):
    def __init__(self, x, y, color, *groups, speed_multiplier=10):
        super().__init__(*groups)
        self.color = color
        self.image = pg.transform.scale(
            pg.image.load(os.path.join("Assets\Images", f"ghost_{self.color}.png")),
            (637 / 20, 673 / 20),
        ).convert_alpha()
        self.image1 = self.image
        self.image2 = pg.transform.scale(
            pg.image.load(os.path.join("Assets\Images", f"ghost_{self.color}2.png")),
            (637 / 20, 673 / 20),
        ).convert_alpha()
        self.sprites = (self.image1, self.image2)
        self.rect = self.image1.get_rect(center=(x,y))
        self.pos = self.rect.center
        self.speed = speed_picker[color] * log10(speed_multiplier)
        self.direction = pg.math.Vector2(0, 0)
        self.path = []
        self.collision_rects = []
        self.current_image = 0

    def findpath(self, map, pos):
        grid = Grid(matrix=map)
        x_pos, y_pos = get_cell(self.rect.center)
        self.start = grid.node(x_pos, y_pos)
        self.end = grid.node(pos[0], pos[1])
        self.start_coords, self.end_coords = ((x_pos, y_pos), (pos[0], pos[1]))
        finder = AStarFinder()
        self.path, _ = finder.find_path(self.start, self.end, grid)
        if self.rect.center == get_coord(x_pos, y_pos):
            self.draw_path()
            self.get_direction()
        self.update()
        grid.cleanup()

    def get_direction(self):
        if len(self.path) > 1:
            self.direction = (
                pg.math.Vector2(self.directors[1]) - pg.math.Vector2(self.directors[0])
            ).normalize()
        else:
            self.direction = pg.math.Vector2(0, 0)

    def update(self):
        self.animefy()
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

    def draw_path(self):
        if len(self.path) > 1:
            self.points = []
            for point in self.path:
                x, y = get_coord(point[0], point[1])
                self.points.append((x, y))
            self.directors = (self.path[0], self.path[1])

    def wall_collide(self, group):
        if pg.sprite.spritecollide(self, group, False):
            for sprite in group:
                if (
                    self.direction.x < 0
                    and abs(sprite.rect.right - self.rect.left) <= 5
                ):
                    self.rect.left = sprite.rect.right + 5
                    self.direction = -self.direction
                if (
                    self.direction.x > 0
                    and abs(sprite.rect.left - self.rect.right) <= 5
                ):
                    self.rect.right = sprite.rect.left - 5
                    self.direction = -self.direction
                if (
                    self.direction.y < 0
                    and abs(sprite.rect.bottom - self.rect.top) <= 5
                ):
                    self.rect.top = sprite.rect.bottom + 5
                    self.direction = -self.direction
                if (
                    self.direction.y > 0
                    and abs(sprite.rect.top - self.rect.bottom) <= 5
                ):
                    self.rect.bottom = sprite.rect.top - 5
                    self.direction = -self.direction

    def animefy(self) -> None:
        """Handles the animations for the Ghosts"""
        self.current_image += self.speed / 30
        if self.current_image >= len(self.sprites):
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


class DisplayingName(pg.sprite.Sprite):
    def __init__(self, x, y, images, *groups):
        super().__init__(*groups)
        self.sprites = images
        self.x, self.y = x, y
        self.current_image = 0
        self.image = self.sprites[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, speed=0, direction=(0,0), switch = False):
        if switch:
            self.current_image += 1
        if direction != (0,0):
            self.move(direction)
        self.current_image += speed
        if self.current_image >= len(self.sprites):
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]
    
    def move(self, direction):
        self.rect.x += 20*direction[0]
        self.rect.y += 20*direction[1]


class PowerPellets(pg.sprite.Sprite):
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.x, self.y = x, y
        self.image = pg.image.load(os.path.join("Assets\Images", "pellet.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Walls(pg.sprite.Sprite):
    def __init__(
        self, w_type: str, pos: tuple, colour: str = "dark_teal", *group: list
    ) -> None:
        """Creates Walls

        Args:
            w_type (str): an entry from walls_type dict
            pos(tuple): coordinates
            *group (list): a group
            colour (str, optional): an entry from colours dict. Defaults to 'dark_teal'.
        """
        super().__init__(*group)
        self.image = pg.Surface(walls_type[w_type])
        self.image.fill(colours[colour])
        self.rect = self.image.get_rect(topleft=pos)


class GameState:
    def __init__(self) -> None:
        self.run = True
        self.player_name = 'Player_1'
        self.state = "initialisation"
        self.revertable_state = "pause_menu"
        self.pacman = Pacman(
            SWIDTH - 100,
            SHEIGHT / 2 + 2 * game_name_height,
            pacman_init_image,
            pacman_group,
        )
        self.initialisation_text = DisplayingName(
            SWIDTH / 2 - game_name_width / 2,
            SHEIGHT / 2 - game_name_height / 2,
            [game_name] * 3 + [game_name_blink],
            current_display,
        )
        self.level_clear = False
        self.level_number = 0
        self.dis_level = dis_level
        self.music = True
        self.backspace = False
        self.delayed_backspace = False
        self.last_map = visible_obstacles
        self.prohibited_keys = (pg.K_ESCAPE, pg.K_TAB)
        self.t_original = 0

    def scene_manager(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if event.type == END_MUSIC:
                match self.state:
                    case 'level 1':
                        pg.mixer.music.load(os.path.join("Assets\Music", "game_music.wav"))
                    case 'finish':
                        pg.mixer.music.load(os.path.join("Assets\Music", "Track 3.wav"))
                    case _:
                        pg.mixer.music.load(os.path.join("Assets\Music", "Funk in G Major.wav"))
                pg.mixer.music.play(-1)

            elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE and self.state == 'level 1':
                self.music = True
                self.revertable_state, self.state = self.state, self.revertable_state
            elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE and self.state == 'information':
                self.player_name = ''
                self.state = 'start_menu'
            elif self.state == 'information':
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.backspace = True
                        self.delayed_backspace = True
                        self.t_original = time()
                    elif event.key != pg.K_RETURN:
                        if event.key not in self.prohibited_keys and len(self.player_name)<16:
                            self.player_name += event.unicode
                            self.player_name = self.player_name.upper()
                    else:
                        if len(self.player_name) > 0 and set(self.player_name) != {' '}:
                            self.music = True
                            self.init_before_level('level 1')
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_BACKSPACE:
                        self.backspace = False
                        self.delayed_backspace = False
                        self.t_original=0
        match self.state:
            case "initialisation":
                self.initialisation()
            case "initialisation_2":
                self.initialisation_2()
            case 'start_menu':
                if self.music:
                    pg.mixer.music.fadeout(1000)
                    pg.mixer.music.load(os.path.join("Assets\Music", "Funk in G Major.wav"))
                    pg.mixer.music.play(-1)
                    self.music = False
                self.start_menu()
            case 'settings':
                self.settings()
            case 'information':
                self.information()
            case "level 1":
                if self.music:
                    pg.mixer.music.fadeout(1000)
                    self.music = False
                self.level_1()
            case "pause_menu":
                if self.music:
                    pg.mixer.music.fadeout(1000)
                    self.music = False
                self.pause_menu()
            case "end":
                self.end()
            case 'finish':
                if self.music:
                    pg.mixer.music.fadeout(1000)
                    self.music = False
                self.finish()
        pg.display.update()

    def initialisation(self):
        screen.fill(colours["dark_grey"])
        if self.pacman.rect.centerx > -(self.pacman.rect.w // 2 + 20):
            screen.fill(
                colours["black"],
                (
                    self.pacman.rect.centerx - self.pacman.rect.w // 2 - 20,
                    self.pacman.rect.centery - self.pacman.rect.h // 2,
                    SWIDTH - self.pacman.rect.centerx + self.pacman.rect.w // 2 + 20,
                    self.pacman.rect.h,
                ),
            )
            current_display.update(0.25)
            current_display.draw(screen)
            self.pacman.move_direction((-1,0))
            pacman_group.update(self.state)
            pacman_group.draw(screen)
            sleep(0.1)
        else:
            self.state = 'initialisation_2'

    def initialisation_2(self):
        screen.fill(colours['dark_grey'])
        if self.initialisation_text.rect.topleft[0] < SWIDTH:
                current_display.update(0, (1,0))
        else:
            Walls('start_H', (SWIDTH/20, SHEIGHT/10), 'light_yellow', start_menu_frames)
            Walls('start_H', (SWIDTH/20, 9*SHEIGHT/10), 'light_yellow', start_menu_frames)
            Walls('start_V', (SWIDTH/20, SHEIGHT/10), 'light_yellow', start_menu_frames)
            Walls('start_V', (9*SWIDTH/20, SHEIGHT/10), 'light_yellow', start_menu_frames)
            start_menu_map = rand_level_maker(start_num_row,start_num_col)
            self.play_button = Button('Play', (3*SWIDTH/4, SHEIGHT/4), InGame_FONT,color=colours['light_orange'])
            self.settings_button = Button('Settings', (3*SWIDTH/4, 2*SHEIGHT/4), InGame_FONT,color=colours['light_orange'])
            self.resume_button = Button('Resume', (SWIDTH/2, SHEIGHT/4), InGame_FONT, color=colours['turquoise'])
            self.pause_settings_button = Button('Settings', (SWIDTH/2, 2*SHEIGHT/4), InGame_FONT, color=colours['turquoise'])
            self.end_button = Button('Exit', (SWIDTH/2, 3*SHEIGHT/4), InGame_FONT,color=colours['turquoise'])
            self.exit_button = Button('Exit', (3*SWIDTH/4, 3*SHEIGHT/4), InGame_FONT,color=colours['light_orange'])
            self.start_buttons = (self.play_button, self.settings_button, self.exit_button)
            self.button_info = [0,0]
            self.pacman = Pacman(
                SWIDTH/20 + self.pacman.rect.w // 2,
                SHEIGHT/10 + self.pacman.rect.h // 2,
                pacman_right,
                pacman_group,
                score=self.pacman.score,
            )
            for row_index, row in enumerate(start_menu_map):
                for col_index, col in enumerate(row):
                    x = SWIDTH/20 + 3 + col_index * (40*SWIDTH/100) / start_num_row
                    y = (SHEIGHT/10 + row_index
                        * (80*SHEIGHT/100)
                        / start_num_col
                    )
                    if col == "v":
                        Walls("menu_V", (x, y),'light_yellow', start_menu_frames)
                    elif col == "h":
                        Walls("menu_H", (x, y),'light_yellow', start_menu_frames)
            self.state = 'start_menu'
        pacman_group.update(self.state)
        pacman_group.draw(screen)
        current_display.draw(screen)
        sleep(0.1)

    def start_menu(self):
        screen.fill(colours['dark_grey'])
        start_menu_frames.draw(screen)
        self.button_info = menu_cycle(self.start_buttons, self.button_info)
        for button in self.start_buttons:
            if button.released:
                match button.text:
                    case 'Play':
                        name = MONOSPACE_FONT.render(f'Name:{self.player_name}', 1, colours["light_orange"])
                        DisplayingName(SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height(), [name], current_display)
                        self.name_border_points = ((SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height()), (19*SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height()), (19*SWIDTH/20 , 5*SHEIGHT/12), (SWIDTH/20,5*SHEIGHT/12))
                        self.state = 'information'
                    case 'Settings':
                        self.previous_settings_window = self.state
                        self.state = 'settings'
                    case 'Exit':
                        self.state = 'end'
                    case _:
                        pass
                self.music_button = SettingsButton('Music', (SWIDTH/2, SHEIGHT/4), END_FONT,color=colours['light_yellow'])
                self.reset_button = Button('Reset Scores', (SWIDTH/2, 2*SHEIGHT/4), END_FONT, color=colours['light_yellow'])
                self.back_button = Button('Back', (SWIDTH/2, 3*SHEIGHT/4), END_FONT,color=colours['light_yellow'])
                self.settings_buttons = (self.music_button, self.reset_button, self.back_button)
        pacman_group.update(self.state)
        self.pacman.wall_collide(start_menu_frames)
        pacman_group.draw(screen)
        self.settings_button.update()
        self.play_button.update()
        self.exit_button.update()

    def settings(self):
        screen.fill(colours['black'])
        self.button_info = menu_cycle(self.settings_buttons, self.button_info)
        self.music_button.update()
        self.reset_button.update()
        self.back_button.update()
        for button in self.settings_buttons[1:]:
            if button.released:
                match button.text:
                    case 'Reset Scores':
                        pass
                    case 'Back':
                        self.state = self.previous_settings_window
        if self.music_button.selected:
            pg.mixer.music.set_volume(1)
        else:
            pg.mixer.music.set_volume(0)

    def information(self):
        del_time = time()-self.t_original
        if (del_time>0.3) and self.delayed_backspace:
            self.player_name = self.player_name[:-1]
        if self.backspace:
            self.player_name = self.player_name[:-1]
            self.backspace = False
        name = MONOSPACE_FONT.render(f'Name:{self.player_name}', 1, colours["light_orange"])
        DisplayingName(SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height(), [name], current_display)
        pg.draw.lines(screen, colours['black'], True, self.name_border_points, 10)
        screen.fill(colours['dark_blue'], (self.name_border_points[0][0],self.name_border_points[0][1], 18*SWIDTH/20, MONOSPACE_FONT.get_height()))
        current_display.update(speed=0)
        current_display.draw(screen)

    def init_before_level(self, level):
        self.level_number += 1
        visible_obstacles.empty()
        visible_obstacles_2.empty()
        ghosts_group.empty()
        self.level_clear = False
        self.state = level
        self.pacman = Pacman(
            self.pacman.rect.w // 2,
            self.dis_level.get_height() + self.pacman.rect.h // 2,
            pacman_right,
            pacman_group,
            score=self.pacman.score,
        )
        for _ in range(self.level_number):
            ghost_coords = get_coord(
                2 * (random.randint(4, 6)), 2 * (random.randint(0, 6))
            )
            ghosts_group.add(
                Ghosts(
                    ghost_coords[0],
                    ghost_coords[1],
                    random.choice(tuple(speed_picker.keys())),
                    speed_multiplier=(self.level_number + 10),
                )
            )
        self.level_1_setup()

    def level_1_setup(self):
        self.counter = 0
        test_map_1 = rand_level_maker()
        self.obstacles_map_1 = self.map(test_map_1)
        test_map_2 = rand_level_maker()
        self.obstacles_map_2 = self.map(test_map_2)
        setit(num_row)
        self.pacman.condition((0, self.dis_level.get_height(), WIDTH, HEIGHT))
        for row_index, row in enumerate(test_map_1):
            for col_index, col in enumerate(row):
                x = 3 + col_index * WIDTH / num_row
                y = (
                    self.dis_level.get_height()
                    + row_index
                    * (HEIGHT - self.dis_level.get_height())
                    / num_col
                )
                if col == "v":
                    Walls("vertical", (x, y),'dark_teal', visible_obstacles)
                elif col == "h":
                    Walls("horizontal", (x, y),'dark_teal', visible_obstacles)
        for row_index, row in enumerate(test_map_2):
            for col_index, col in enumerate(row):
                x = 3 + col_index * WIDTH / num_row
                y = (
                    self.dis_level.get_height()
                    + row_index
                    * (HEIGHT - self.dis_level.get_height())
                    / num_col
                )
                if col == "v":
                    Walls("vertical", (x, y), 'dark_red', visible_obstacles_2)
                elif col == "h":
                    Walls("horizontal", (x, y), 'dark_red', visible_obstacles_2)
        
        #Framework walls
        Walls('big_H', (0, dis_level_height -3), 'dark_red', visible_obstacles_2)
        Walls('small_H', (0, HEIGHT),  'dark_red', visible_obstacles_2)
        Walls('small_V', (0,dis_level_height), 'dark_red', visible_obstacles_2)
        Walls('big_V', (SWIDTH-3,0), 'dark_red', visible_obstacles_2)
        Walls('small_V', (WIDTH, dis_level_height), 'dark_red', visible_obstacles_2)
        Walls('big_H', (0, dis_level_height -3), 'dark_teal', visible_obstacles)
        Walls('small_H', (0, HEIGHT),  'dark_teal', visible_obstacles)
        Walls('small_V', (0,dis_level_height), 'dark_teal', visible_obstacles)
        Walls('big_V', (SWIDTH-3,0), 'dark_teal', visible_obstacles)
        Walls('small_V', (WIDTH, dis_level_height), 'dark_teal', visible_obstacles)

    def level_1(self):
        self.dis_level = InGame_FONT.render(
            f"Level - {self.level_number}", 1, colours["perk_green"]
        )
        self.display_score = Score_FONT.render(
            f"G:{self.pacman.score}", 1, colours["light_orange"]
        )
        screen.fill(colours["black"])
        screen.fill(colours["dark_grey"], (0, 0, SWIDTH, self.dis_level.get_height()))
        screen.blit(self.dis_level, (WIDTH / 2 - self.dis_level.get_width() / 2, 0))
        screen.blit(
            self.display_score,
            (
                SWIDTH - 1.5 * self.display_score.get_width(),
                self.dis_level.get_height() / 2 - self.display_score.get_height() / 2,
            ),
        )
        pellet_group.draw(screen)
        if not self.level_clear and len(pellet_group) == 0:
            self.level_clear = True
            self.pacman.temp_switch = True
        if not len(pellet_group) == 0:
            self.map_toggle()
            ghosts_group.draw(screen)
        else:
            self.last_map.draw(screen)
            if self.pacman.rect.y > SHEIGHT + self.pacman.rect.width // 2:
                sleep(1)
                self.init_before_level("level 1")
        if self.pacman.ghost_collide():
            self.state = "end"
            sleep(0.5)
        self.pacman.get_score(pellet_group)
        pacman_group.update(self.state)
        pacman_group.draw(screen)

    def map_toggle(self):
        self.counter += 1
        if self.counter > 500:
            self.counter = 0
        if self.counter > 250:
            visible_obstacles.draw(screen)
            self.last_map = visible_obstacles
            for ghost in ghosts_group.sprites():
                ghost.wall_collide(visible_obstacles)
                ghost.findpath(self.obstacles_map_1, get_cell(self.pacman.rect.center))
            self.pacman.wall_collide(visible_obstacles)
        else:
            visible_obstacles_2.draw(screen)
            self.last_map = visible_obstacles_2
            for ghost in ghosts_group.sprites():
                ghost.wall_collide(visible_obstacles_2)
                ghost.findpath(self.obstacles_map_2, get_cell(self.pacman.rect.center))
            self.pacman.wall_collide(visible_obstacles_2)

    def pause_menu(self):
        screen.fill(colours['light_yellow'], (2*SWIDTH/10, dis_level_height + 1.275*(HEIGHT- dis_level_height)/10 - self.play_button.image.get_width()/2, 3*SWIDTH/5, 7.45*(HEIGHT- dis_level_height)/10 + self.play_button.image.get_width()))
        self.button_info = menu_cycle([self.resume_button, self.pause_settings_button, self.end_button], self.button_info)
        if self.resume_button.released:
            pg.mixer.music.fadeout(1000)
            self.state, self.revertable_state = self.revertable_state, self.state
        elif self.pause_settings_button.released:
            self.previous_settings_window = self.state
            self.state = 'settings'
        elif self.end_button.released:
            self.state = 'end'
        self.pause_settings_button.update()
        self.resume_button.update()
        self.end_button.update()

    def map(self, test_map):
        map = [
            [1 for _ in range(2 * num_row - 1)]
            for _ in range(2 * num_col - 1)
        ]
        for col, walls_list in enumerate(test_map):
            for row, walls in enumerate(walls_list):
                if walls == "h":
                    map[2 * col - 1][2 * row] = 0
                elif walls == "v":
                    map[2 * col][2 * row - 1] = 0
        for x in range(1, len(map), 2):
            for y in range(1, len(map), 2):
                map[x][y] = 0
        return map

    def end(self):
        name = Name_FONT.render(f'NAME: {self.player_name}', 1, colours["light_orange"])
        text = END_FONT.render(f'Your Score : {self.pacman.score}', 1, colours['light_yellow'])
        text_2 = END_FONT.render(f'Press Esc to Exit', 1, colours['light_yellow'])
        DisplayingName((SWIDTH/2) - name.get_width()/2,SHEIGHT/4 - name.get_height()/2, [name], multiple_displays)
        DisplayingName((SWIDTH/2) - text.get_width()/2,3*SHEIGHT/5 - text.get_height()/2, [text], multiple_displays)
        DisplayingName((SWIDTH/2) - text_2.get_width()/2,4*SHEIGHT/5 - text_2.get_height()/2, [text_2], multiple_displays)
        self.state = 'finish'
        self.music = True
    
    def finish(self):
        screen.fill(colours["dark_grey"])
        multiple_displays.update(speed = 0)
        multiple_displays.draw(screen)
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            self.run = False