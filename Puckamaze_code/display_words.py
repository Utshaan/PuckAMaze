import pygame as pg

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