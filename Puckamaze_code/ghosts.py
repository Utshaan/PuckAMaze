from screen import *
from math import log10
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from functions import get_cell, get_coord

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
