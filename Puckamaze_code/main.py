from gamecode import GameState, pg, os
import sys
from ftp_protocol import update_site

FPS = 60
clock = pg.time.Clock()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

game_state = GameState()
dx, dy = 0, 0
while game_state.run:
    clock.tick(FPS)
    game_state.scene_manager()

update_site()
