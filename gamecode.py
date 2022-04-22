from screen import *
from ftp_protocol import update_site
from pacman import Pacman
from display_words import DisplayingName
from time import time, sleep
from walls import Walls
from functions import *
from buttons import Button, SettingsButton
from ghosts import Ghosts
from random import randint, choice
from py_to_html import Html_handler
from py_to_json import JSON_handler, json

class GameState:
    def __init__(self) -> None:
        self.run = True
        self.player_name = 'PLAYER_1'
        self.player_passw = ''
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
        self.prohibited_keys = (pg.K_ESCAPE, pg.K_TAB, pg.K_SPACE)
        self.t_original = 0
        self.name_condition_singlepress = False
        with open(resource_path('Assets/passwords.json')) as file:
            self.password_checker = JSON_handler(file)

    def scene_manager(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if event.type == END_MUSIC:
                match self.state:
                    case 'level 1':
                        pg.mixer.music.load(resource_path("Assets/Music/game_music.wav"))
                    case 'finish':
                        pg.mixer.music.load(resource_path("Assets/Music/Track 3.wav"))
                    case _:
                        pg.mixer.music.load(resource_path("Assets/Music/Funk in G Major.wav"))
                pg.mixer.music.play(-1)

            elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE and self.state == 'level 1':
                self.music = True
                self.revertable_state, self.state = self.state, self.revertable_state
            elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE and self.state == 'information':
                self.player_name = ''
                self.state = 'start_menu'
            elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE and self.state == 'password':
                self.player_passw = ''
                self.state = 'information'
            elif self.state == 'information':
                if event.type == pg.KEYDOWN:
                    if not self.name_condition_singlepress:
                        self.player_name = ''
                        self.name_condition_singlepress = True
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
                            self.state = 'password'
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_BACKSPACE:
                        self.backspace = False
                        self.delayed_backspace = False
                        self.t_original=0
            elif self.state == 'password':
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.backspace = True
                        self.delayed_backspace = True
                        self.t_original = time()
                    elif event.key != pg.K_RETURN:
                        if event.key not in self.prohibited_keys and len(self.player_passw)<16:
                            self.player_passw += event.unicode
                    else:
                        if len(self.player_passw) > 0 and set(self.player_passw) != {' '} and self.password_checker.check(self.player_name, self.player_passw):
                            self.music = True
                            self.init_before_level('level 1')
                        else:
                            self.state = 'information'
                            self.player_passw = ''
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_BACKSPACE:
                        self.backspace = False
                        self.delayed_backspace = False
                        self.t_original=0
            elif self.state == 'reseting password':
                if self.reset_scene == 'name':
                    if event.type == pg.KEYDOWN:
                        if not self.name_condition_singlepress:
                            self.player_name = ''
                            self.name_condition_singlepress = True
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
                                self.reset_scene = 'old_p'
                    elif event.type == pg.KEYUP:
                        if event.key == pg.K_BACKSPACE:
                            self.backspace = False
                            self.delayed_backspace = False
                            self.t_original=0
                elif self.reset_scene == 'old_p':
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.backspace = True
                            self.delayed_backspace = True
                            self.t_original = time()
                        elif event.key != pg.K_RETURN:
                            if event.key not in self.prohibited_keys and len(self.player_passw)<16:
                                self.player_passw += event.unicode
                        else:
                            if len(self.player_passw) > 0 and set(self.player_passw) != {' '} and self.password_checker.check(self.player_name, self.player_passw):
                                self.reset_scene = 'new_p'
                                self.player_passw = ''
                            else:
                                self.reset_scene = 'name'
                                self.player_passw = ''
                    elif event.type == pg.KEYUP:
                        if event.key == pg.K_BACKSPACE:
                            self.backspace = False
                            self.delayed_backspace = False
                            self.t_original=0
                if self.reset_scene == 'new_p':
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.backspace = True
                            self.delayed_backspace = True
                            self.t_original = time()
                        elif event.key != pg.K_RETURN:
                            if event.key not in self.prohibited_keys and len(self.player_passw)<16:
                                self.player_passw += event.unicode
                        else:
                            if len(self.player_passw) > 0 and set(self.player_passw) != {' '}:
                                self.music = True
                                self.state = 'settings'
                                self.password_checker.update(self.player_name, self.player_passw)
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
                    pg.mixer.music.load(resource_path("Assets/Music/Funk in G Major.wav"))
                    pg.mixer.music.play(-1)
                    self.music = False
                self.start_menu()
            case 'settings':
                self.settings()
            case 'information':
                self.information()
            case 'password':
                self.password()
            case 'reseting password':
                self.reseting_password()
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
            self.button_info = [[0,0], [0,0],[0,0]]
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
            self.music_button = SettingsButton('Music', (SWIDTH/2, SHEIGHT/4), END_FONT,color=colours['light_yellow'])
            self.reset_button = Button('Reset Password', (SWIDTH/2, 2*SHEIGHT/4), END_FONT, color=colours['light_yellow'])
            self.back_button = Button('Back', (SWIDTH/2, 3*SHEIGHT/4), END_FONT,color=colours['light_yellow'])
            self.settings_buttons = (self.music_button, self.reset_button, self.back_button)
        pacman_group.update(self.state)
        pacman_group.draw(screen)
        current_display.draw(screen)
        sleep(0.1)

    def start_menu(self):
        screen.fill(colours['dark_grey'])
        start_menu_frames.draw(screen)
        self.button_info[0] = menu_cycle(self.start_buttons, self.button_info[0])
        for button in self.start_buttons:
            if button.released:
                self.name_border_points = ((SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height()), (19*SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height()), (19*SWIDTH/20 , 5*SHEIGHT/12), (SWIDTH/20,5*SHEIGHT/12))
                match button.text:
                    case 'Play':
                        name = MONOSPACE_FONT.render(f'Name:{self.player_name}', 1, colours["light_orange"])
                        DisplayingName(SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height(), [name], current_display)
                        self.state = 'information'
                    case 'Settings':
                        self.previous_settings_window = self.state
                        self.state = 'settings'
                    case 'Exit':
                        self.state = 'end'
                    case _:
                        pass
        pacman_group.update(self.state)
        self.pacman.wall_collide(start_menu_frames)
        pacman_group.draw(screen)
        self.settings_button.update()
        self.play_button.update()
        self.exit_button.update()

    def settings(self):
        screen.fill(colours['black'])
        self.button_info[1] = menu_cycle(self.settings_buttons, self.button_info[1])
        self.music_button.update()
        self.reset_button.update()
        self.back_button.update()
        for button in self.settings_buttons[1:]:
            if button.released:
                match button.text:
                    case 'Reset Password':
                        self.state = 'reseting password'
                        self.reset_scene = 'name'
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

    def password(self):
        del_time = time()-self.t_original
        if (del_time>0.3) and self.delayed_backspace:
            self.player_passw = self.player_passw[:-1]
        if self.backspace:
            self.player_passw = self.player_passw[:-1]
            self.backspace = False
        passw = MONOSPACE_FONT.render(f'Passw:{self.player_passw}', 1, colours["light_orange"])
        DisplayingName(SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height(), [passw], current_display)
        pg.draw.lines(screen, colours['black'], True, self.name_border_points, 10)
        screen.fill(colours['dark_blue'], (self.name_border_points[0][0],self.name_border_points[0][1], 18*SWIDTH/20, MONOSPACE_FONT.get_height()))
        current_display.update(speed=0)
        current_display.draw(screen)

    def reseting_password(self):
        if self.reset_scene == 'name':
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
        if self.reset_scene == 'old_p':
            del_time = time()-self.t_original
            if (del_time>0.3) and self.delayed_backspace:
                self.player_passw = self.player_passw[:-1]
            if self.backspace:
                self.player_passw = self.player_passw[:-1]
                self.backspace = False
            passw = MONOSPACE_FONT.render(f'Old P:{self.player_passw}', 1, colours["light_orange"])
            DisplayingName(SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height(), [passw], current_display)
            pg.draw.lines(screen, colours['black'], True, self.name_border_points, 10)
            screen.fill(colours['dark_blue'], (self.name_border_points[0][0],self.name_border_points[0][1], 18*SWIDTH/20, MONOSPACE_FONT.get_height()))
            current_display.update(speed=0)
            current_display.draw(screen)
        if self.reset_scene == 'new_p':
            del_time = time()-self.t_original
            if (del_time>0.3) and self.delayed_backspace:
                self.player_passw = self.player_passw[:-1]
            if self.backspace:
                self.player_passw = self.player_passw[:-1]
                self.backspace = False
            passw = MONOSPACE_FONT.render(f'New P:{self.player_passw}', 1, colours["light_orange"])
            DisplayingName(SWIDTH/20, 5*SHEIGHT/12 - MONOSPACE_FONT.get_height(), [passw], current_display)
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
                2 * (randint(4, 6)), 2 * (randint(0, 6))
            )
            ghosts_group.add(
                Ghosts(
                    ghost_coords[0],
                    ghost_coords[1],
                    choice(tuple(speed_picker.keys())),
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
        self.button_info[2] = menu_cycle([self.resume_button, self.pause_settings_button, self.end_button], self.button_info[2])
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
        text_2 = END_FONT.render(f'Press Esc to Sync and Exit', 1, colours['light_yellow'])
        DisplayingName((SWIDTH/2) - name.get_width()/2,SHEIGHT/4 - name.get_height()/2, [name], multiple_displays)
        DisplayingName((SWIDTH/2) - text.get_width()/2,3*SHEIGHT/5 - text.get_height()/2, [text], multiple_displays)
        DisplayingName((SWIDTH/2) - text_2.get_width()/2,4*SHEIGHT/5 - text_2.get_height()/2, [text_2], multiple_displays)
        self.state = 'finish'
        self.music = True
        self.password_checker.update(self.player_name, self.player_passw)
    
    def finish(self):
        screen.fill(colours["dark_grey"])
        multiple_displays.update(speed = 0)
        multiple_displays.draw(screen)
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            if self.player_name != '' and self.pacman.score != 0:
                with open(resource_path("Assets/index.html")) as htmlFile:
                    hhandler = Html_handler(htmlFile)
                hhandler.update(self.pacman.score, self.player_name)
                with open(resource_path("Assets/index.html"), "w", encoding="utf-8") as change_html:
                    change_html.write(str(hhandler.file))
            if self.player_name != '':
                with open(resource_path("Assets/passwords.json"), "w") as change_json:
                    json.dump(self.password_checker.file, change_json, indent=4)
            
            update_site()

            self.run = False