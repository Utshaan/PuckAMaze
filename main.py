from gamecode import GameState, pg

FPS = 60
clock = pg.time.Clock()

game_state = GameState()
dx, dy = 0, 0
while game_state.run:
    clock.tick(FPS)
    game_state.scene_manager()

