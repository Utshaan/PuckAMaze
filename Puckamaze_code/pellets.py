import pygame as pg
import os

class PowerPellets(pg.sprite.Sprite):
    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.x, self.y = x, y
        self.image = pg.image.load(os.path.join("Assets\Images", "pellet.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))