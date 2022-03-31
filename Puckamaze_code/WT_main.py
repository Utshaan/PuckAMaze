import pygame as pg
from pacman import GameState
from screen import *
import os
from time import time
from rich import print


FPS = 60
clock = pg.time.Clock()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

game_state = GameState()
dx, dy = 0, 0
while game_state.run:
    clock.tick(FPS)
    game_state.scene_manager()
