import pygame
from pacman import GameState
from screen import *
import os
from time import time
from rich import print

# from threading import Timer #timer(time, func).start

FPS = 60
clock = pygame.time.Clock()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.mouse.set_visible(True)

game_state = GameState()
hidden_var = -100
dx, dy = 0, 0
while game_state.run:
    events = pygame.event.get()
    clock.tick(FPS)
    game_state.scene_manager()