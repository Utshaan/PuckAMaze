import pygame
from itertools import product
from rich import print
import os
from time import sleep
import random
from pathfinding.core.grid import Grid
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
            dis_level.get_height()
            + ((2 * j + 1) * (HEIGHT - dis_level.get_height()) // (number * 2)),
            pellet_group,
        )

def rand_level_maker() -> None:
    map_level = []
    temp = " "
    for _ in range(num_pel_row_column-1):
            temp += random.choice(shuffle_list[1:5])
    map_level.append(list(temp))
    for _ in range(num_pel_row_column-2):
        s = random.choice([' ','h'])
        for _ in range(num_pel_row_column-2):
            s += random.choice(shuffle_list)
        s += random.choice(shuffle_list[:-1])
        map_level.append(list(s))
    temp = " "
    for _ in range(num_pel_row_column-1):
        temp += random.choice(shuffle_list[1:5])
    map_level.append(list(temp))
    map_level[1][0] = ' '
    return map_level


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image, *groups) -> None:
        """this is the summary

        Args:
            x (int): x coordinate
            y (int): y coordinate
            image (image): Image
            *groups: Groups
        """
        super().__init__(*groups)
        self.to_animate = True
        self.current_image = 0
        self.score = 0
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.animating_list = [self.image, pac_close]
        self.limit = (0, 0, SWIDTH, SHEIGHT)
        self.direction = pygame.math.Vector2()
        self.temp_switch = False

    def move_left(self) -> None:
        self.rect.x -= 20

    def update(self, scene: str) -> None:
        """Updating the object

        Args:
            pos (tuple): (abcissa,ordinate)
            scene (str): GameState.scene
        """
        self.control()
        if scene == "initialisation":
            self.animefy([pacman_init_image, pacman_init_close])
        elif scene == "level 1":
            if self.temp_switch:
                self.temp_switch = False
                self.condition((WIDTH, dis_level.get_height(), SWIDTH, SHEIGHT + 2*self.rect.height))
                self.rect.topleft = (WIDTH + 3, dis_level.get_height())
            self.animefy(self.animating_list, 0.05)

    def animefy(self, images, speed=0.2) -> None:
        """Handles all animations of the objects

        Args:
            image (list): The list of images to animate through
            scene (str): GameState.state
        """
        self.sprites = images
        if self.to_animate:
            self.current_image += speed
            if self.current_image > len(self.sprites):
                self.current_image = 0
            self.image = self.sprites[int(self.current_image)]

    def check_collide(self, group) -> None:
        """Checks if the object has collided with any other object and increments the score by one.

        Args:
            group (group): The group to check collision with
        """
        if pygame.sprite.spritecollide(self, group, True):
            self.score += 1
        
    def wall_collide(self, group) -> None:
        """check collision with walls in particular

        Args:
            group (group): Gamestate.state
        """
        for sprite in group:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0 and abs(sprite.rect.right - self.rect.left)<= 5:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0 and abs(sprite.rect.left - self.rect.right)<= 5:
                    self.rect.right = sprite.rect.left
                if self.direction.y < 0 and abs(sprite.rect.bottom - self.rect.top)<= 5:
                    self.rect.top = sprite.rect.bottom
                if self.direction.y > 0 and abs(sprite.rect.top - self.rect.bottom)<= 5:
                    self.rect.bottom = sprite.rect.top

    def control(self) -> None:
        """checks for all controls. needs no inputs"""
        self.direction.x, self.direction.y = 0,0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x += -1
            self.animating_list = [pacman_left, pac_close]
            if self.rect.x - 5 > self.limit[0]:
                self.rect.x += -5
        if keys[pygame.K_s]:
            self.direction.y += 1
            self.animating_list = [pacman_down, pac_close_R]
            if self.rect.y + 5 < self.limit[3] - self.rect.h:
                self.rect.y += 5
        if keys[pygame.K_d]:
            self.direction.x += 1
            self.animating_list = [pacman_right, pac_close_R]
            if self.rect.x + 5 < self.limit[2] - self.rect.w:
                self.rect.x += 5
        if keys[pygame.K_w]:
            self.direction.y += -1
            self.animating_list = [pacman_up, pac_close]
            if self.rect.y - 5 > self.limit[1]:
                self.rect.y += -5


    def condition(self, rect_coords: tuple) -> None:
        """Confines object in a certain section

        Args:
            rect_coords (tuple) : (X1,Y1,X2,Y2)
        """
        self.limit = rect_coords

class Ghosts(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *groups):
        super().__init__(*groups)
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"ghost_{self.color}.png")), (637/20, 673/20))
        self.rect = self.image.get_rect(center=(x,y))
    
    def findpath(self):
        pass

class DisplayingName(pygame.sprite.Sprite):
    def __init__(self, x, y, images, *groups):
        super().__init__(*groups)
        self.sprites = images
        self.x, self.y = x, y
        self.to_animate = False
        self.current_image = 0
        self.image = self.sprites[int(self.current_image)]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, speed):
        if self.to_animate:
            self.current_image += speed
            if self.current_image >= len(self.sprites):
                self.current_image = 0
            self.image = self.sprites[int(self.current_image)]


class PowerPellets(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.x, self.y = x, y
        self.image = pygame.image.load(
            os.path.join("Assets", "pellet.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Walls(pygame.sprite.Sprite):
    def __init__(self, w_type:str,pos:tuple, *group: list, colour:str = 'dark_teal') -> None:
        """Creates Walls

        Args:
            w_type (str): an entry from walls_type dict
            pos(tuple): coordinates
            *group (list): a group
            colour (str, optional): an entry from colours dict. Defaults to 'dark_teal'.
        """
        super().__init__(*group)
        self.image = pygame.Surface(walls_type[w_type])
        self.image.fill(colours[colour])
        self.rect = self.image.get_rect(topleft=pos)


class GameState:
    def __init__(self) -> None:
        self.run = True
        self.state = "initialisation"
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
        self.test_map_1, self.test_map_2 = [],[]

    def scene_manager(self) -> None:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.run = False
        match self.state:
            case "initialisation":
                self.initialisation()
            case "level 1":
                self.level_1()
            case "end":
                self.end()

    def initialisation(self):
        screen.fill(colours["dark_grey"])
        self.initialisation_text.to_animate = True
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
            self.pacman.move_left()
            pacman_group.update(self.state)
            pacman_group.draw(screen)
            sleep(0.1)
        else:
            self.init_before_level('level 1')
        pygame.display.update()

    def level_1(self):
        self.dis_level = InGame_FONT.render(f"Level - {self.level_number}", 1, colours["perk_green"])
        screen.fill(colours["black"])
        screen.fill(colours["dark_grey"], (0, 0, SWIDTH, self.dis_level.get_height()))
        screen.blit(self.dis_level, (WIDTH / 2 - self.dis_level.get_width() / 2, 0))
        pygame.draw.line(
            screen,
            colours["dark_teal"],
            (WIDTH, self.dis_level.get_height()),
            (WIDTH, HEIGHT),
            3,
        )
        pygame.draw.line(
            screen, colours["dark_teal"], (0, self.dis_level.get_height()), (0, HEIGHT), 3
        )
        pygame.draw.line(
            screen,
            colours["dark_teal"],
            (0, self.dis_level.get_height()),
            (SWIDTH, self.dis_level.get_height()),
            3,
        )
        pygame.draw.line(
            screen, colours["dark_teal"], (0, HEIGHT), (SWIDTH, HEIGHT), 3
        ) if len(pellet_group) != 0 else pygame.draw.line(
            screen, colours["dark_teal"], (0, HEIGHT), (WIDTH, HEIGHT), 3
        ) and pygame.draw.line(
            screen, colours["dark_teal"], (WIDTH, HEIGHT), (WIDTH, SHEIGHT), 3
        )
        pygame.draw.line(
            screen, colours["dark_teal"], (SWIDTH - 1.5, 0), (SWIDTH - 1.5, SHEIGHT), 3
        )
        pellet_group.draw(screen)
        if not self.level_clear and len(pellet_group) == 0:
            self.level_clear = True
            self.pacman.temp_switch = True
        if not len(pellet_group) == 0:
            self.map_toggle()
        else:
            if self.pacman.rect.y > SHEIGHT + self.pacman.rect.width//2:
                sleep(1)
                self.init_before_level('level 1')
        self.pacman.check_collide(pellet_group)
        pacman_group.update(self.state)
        pacman_group.draw(screen)
        pygame.display.update()

    def level_1_setup(self):
        self.counter = 0
        self.test_map_1 = rand_level_maker()
        self.test_map_2 = rand_level_maker()
        setit(num_pel_row_column)
        self.pacman.condition((0, self.dis_level.get_height(), WIDTH, HEIGHT))
        for row_index,row in enumerate(self.test_map_1):
            for col_index, col in enumerate(row):
                x = 3 + col_index*WIDTH/num_pel_row_column
                y = self.dis_level.get_height()+  row_index*(HEIGHT-self.dis_level.get_height())/num_pel_row_column
                if col == 'v':
                    Walls('vertical',(x,y), visible_obstacles, third_group)
                elif col == 'h':
                    Walls('horizontal',(x,y), visible_obstacles, third_group)
        for row_index,row in enumerate(self.test_map_2):
            for col_index, col in enumerate(row):
                x = 3 + col_index*WIDTH/num_pel_row_column
                y = self.dis_level.get_height()+  row_index*(HEIGHT-self.dis_level.get_height())/num_pel_row_column
                if col == 'v':
                    Walls('vertical',(x,y), visible_obstacles_2, third_group)
                elif col == 'h':
                    Walls('horizontal',(x,y), visible_obstacles_2, third_group)

    def map_toggle(self):
        self.counter += 1
        if self.counter > 500:
            self.counter =0
        if self.counter > 250:
            visible_obstacles.draw(screen)
            self.pacman.wall_collide(visible_obstacles)
        else:
            visible_obstacles_2.draw(screen)
            self.pacman.wall_collide(visible_obstacles_2)

    def init_before_level(self, level):
        self.level_number += 1
        visible_obstacles.empty();visible_obstacles_2.empty()
        self.level_clear = False
        self.state = level
        self.pacman = Pacman(
            self.pacman.rect.w // 2,
            self.dis_level.get_height() + self.pacman.rect.h // 2,
            pacman_right,
            pacman_group,
        )
        self.level_1_setup()

    def end(self):
        screen.blit(background, (0, 0))
        pygame.display.update()
        sleep(3)
        self.run = False

    def map(self, test_map):
        map = [[1 for _ in range(13)] for _ in range(13)]
        for col,walls_list in enumerate(test_map):
            for row,walls in enumerate(walls_list):
                if walls == 'h':
                    map[2*col-1][2*row] = 0
                elif walls == 'v':
                    map[2*col][2*row -1] = 0
        for x in range(1,len(map),2):
            for y in range(1,len(map),2):
                map[x][y] = 0
