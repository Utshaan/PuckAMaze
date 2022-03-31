import pygame as pg
import os

pg.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 600, 500
SWIDTH, SHEIGHT = 700, 515
screen = pg.display.set_mode((SWIDTH, SHEIGHT), pg.RESIZABLE)

colours = dict(
    black=(0, 0, 0),
    light_orange=(236, 134, 87),
    perk_green=(155, 255, 0),
    turquoise=(12, 126, 158),
    dark_grey=(23, 23, 23),
    dark_teal=(14, 120, 120),
)

speed_picker = dict(red=0.8, pink=1, green=0.9)

InGame_FONT = pg.font.SysFont("couriernew", 50)
DISPLAY_FONT = pg.font.Font(os.path.join("Assets", "PAC-FONT.TTF"), 80)
Score_FONT = pg.font.SysFont("couriernew", 30)
game_name_blink = DISPLAY_FONT.render("Mr.Pacman", 1, colours["black"])
game_name = DISPLAY_FONT.render("Mr.Pacman", 1, colours["light_orange"])
game_name_width, game_name_height = game_name.get_width(), game_name.get_height()
dis_level = InGame_FONT.render(f"Level - 1", 1, colours["perk_green"])
dis_level_height = dis_level.get_height()
# background = pg.transform.scale(
#     pg.image.load(os.path.join("Assets", "map.jpg")), (SWIDTH, SHEIGHT)
# )
icon = pg.image.load(os.path.join("Assets", "icon.png"))
not_background_shadow = pg.Rect(0, 0, WIDTH, dis_level.get_height())

pacman_left = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    180,
)
pacman_down = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    270,
)
pacman_right = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    0,
)
pacman_up = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets", "pacman.png")), (673 / 20, 721 / 20)
    ),
    90,
)
pac_close = pg.transform.scale(
    pg.image.load(os.path.join("Assets", "pacman_close.png")), (673 / 20, 721 / 20)
)
pac_close_R = pg.transform.scale(
    pg.image.load(os.path.join("Assets", "pacman_close_R.png")),
    (673 / 20, 721 / 20),
)
pac_last = pacman_right
pellet_image = pg.image.load(os.path.join("Assets", "pellet.png")).convert_alpha()
pacman_init_image = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets", "pacman.png")), (637 / 10, 721 / 10)
    ),
    180,
)
pacman_init_close = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets", "pacman_close.png")),
        (637 / 10, 721 / 10),
    ),
    180,
)

num_pel_row_column = 7

pacman_group = pg.sprite.GroupSingle()
current_display = pg.sprite.GroupSingle()
pellet_group = pg.sprite.Group()
visible_obstacles = pg.sprite.Group()
visible_obstacles_2 = pg.sprite.Group()
ghosts_group = pg.sprite.Group()

walls_type = dict(
    vertical=(3, ((HEIGHT - dis_level.get_height()) / num_pel_row_column) + 3),
    horizontal=((WIDTH / num_pel_row_column) + 3, 3),
)

shuffle_list = (" ", " ", " ", " ", "v", "h", "v", "h")
