from screen import *


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
        self.debug = debug

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
        if self.debug:
            pg.draw.rect(screen, colours['perk_green'], self.rect)

    def get_score(self, group) -> None:
        """Checks if the object has collided with any other object and increments the score by one.

        Args:
            group (group): The group to check collision with
        """
        if pg.sprite.spritecollide(self, group, True):
            self.score += 19

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
        return pg.sprite.groupcollide(pacman_group, ghosts_group, False, False, collided=pg.sprite.collide_rect_ratio(0.88))

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
