import pygame
import os

pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 600, 500
SWIDTH, SHEIGHT = 700, 515
screen = pygame.display.set_mode((SWIDTH, SHEIGHT), pygame.RESIZABLE)

colours = dict(
    black=(0, 0, 0),
    light_orange=(236, 134, 87),
    perk_green=(155, 255, 0),
    turquoise=(12, 126, 158),
    dark_grey=(23, 23, 23),
    dark_teal=(14, 120, 120),
)

speed_picker = dict(
    red = 0.8,
    pink = 1,
    green = 0.9
)

InGame_FONT = pygame.font.SysFont("couriernew", 50)
DISPLAY_FONT = pygame.font.Font(os.path.join("Assets", "PAC-FONT.TTF"), 80)
Score_FONT = pygame.font.SysFont("couriernew", 30)
game_name_blink = DISPLAY_FONT.render("Mr.Pacman", 1, colours["black"])
game_name = DISPLAY_FONT.render("Mr.Pacman", 1, colours["light_orange"])
game_name_width, game_name_height = game_name.get_width(), game_name.get_height()
dis_level = InGame_FONT.render(f"Level - 1", 1, colours["perk_green"])
dis_level_height = dis_level.get_height()
# background = pygame.transform.scale(
#     pygame.image.load(os.path.join("Assets", "map.jpg")), (SWIDTH, SHEIGHT)
# )
icon = pygame.image.load(os.path.join("Assets", "icon.png"))
not_background_shadow = pygame.Rect(0, 0, WIDTH, dis_level.get_height())

pacman_left = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    180,
)
pacman_down = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    270,
)
pacman_right = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    0,
)
pacman_up = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    90,
)
pac_close = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "pacman_close.png")), (673 / 20, 721 / 20)
)
pac_close_R = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "pacman_close_R.png")),
    (673 / 20, 721 / 20),
)
pac_last = pacman_right
pellet_image = pygame.image.load(os.path.join("Assets", "pellet.png")).convert_alpha()
pacman_init_image = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "pacman.png")), (637 / 10, 721 / 10)
    ),
    180,
)
pacman_init_close = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "pacman_close.png")),
        (637 / 10, 721 / 10),
    ),
    180,
)

num_pel_row_column = 7

pacman_group = pygame.sprite.GroupSingle()
current_display = pygame.sprite.GroupSingle()
pellet_group = pygame.sprite.Group()
visible_obstacles = pygame.sprite.Group()
visible_obstacles_2 = pygame.sprite.Group()
ghosts_group = pygame.sprite.Group()

walls_type = dict(
    vertical=(3, ((HEIGHT-dis_level.get_height()) / num_pel_row_column)+3),
    horizontal=((WIDTH / num_pel_row_column)+3, 3),
)

shuffle_list = (' ',' ',' ',' ','v','h','v','h')
