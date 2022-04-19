import sys
import pygame as pg
import os

pg.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 600, 500
SWIDTH, SHEIGHT = 750, 515
screen = pg.display.set_mode((SWIDTH, SHEIGHT), pg.RESIZABLE)

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

colours = dict(
    black=(0, 0, 0),
    dark_red=(179, 12, 0),
    light_orange=(236, 134, 87),
    perk_green=(155, 255, 0),
    turquoise=(12, 126, 158),
    dark_grey=(23, 23, 23),
    dark_teal=(14, 120, 120),
    light_yellow=(255, 235, 149),
    dark_blue=(33, 43, 66),
)

speed_picker = dict(red=0.8, pink=1, green=0.9)

InGame_FONT = pg.font.SysFont("couriernew", 50)
DISPLAY_FONT = pg.font.Font(os.path.join("Assets\Fonts", "PAC-FONT.TTF"), 80)
MONOSPACE_FONT = pg.font.Font(os.path.join("Assets\Fonts", "RobotoMono-Light.ttf"), 50)
END_FONT = pg.font.SysFont('couriernew', 40)
menu_name_FONT = pg.font.SysFont('couriernew', 50)
Score_FONT = pg.font.SysFont("couriernew", 30)
Name_FONT = pg.font.Font(os.path.join("Assets\Fonts", "RobotoMono-LightItalic.ttf"), 50)
game_name_blink = DISPLAY_FONT.render("Mr.Pacman", 1, colours["black"])
game_name = DISPLAY_FONT.render("Mr.Pacman", 1, colours["light_orange"])
game_name_width, game_name_height = game_name.get_width(), game_name.get_height()
dis_level = InGame_FONT.render(f"Level - 1", 1, colours["perk_green"])
dis_level_height = dis_level.get_height()

pacman_left = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets\Images", "pacman.png")), (673 / 20, 721 / 20)
    ),
    180,
).convert_alpha()
pacman_down = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets\Images", "pacman.png")), (673 / 20, 721 / 20)
    ),
    270,
).convert_alpha()
pacman_right = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets\Images", "pacman.png")), (673 / 20, 721 / 20)
    ),
    0,
).convert_alpha()
pacman_up = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets\Images", "pacman.png")), (673 / 20, 721 / 20)
    ),
    90,
).convert_alpha()
pac_close = pg.transform.scale(
    pg.image.load(os.path.join("Assets\Images", "pacman_close.png")), (673 / 20, 721 / 20)
).convert_alpha()
pac_close_R = pg.transform.scale(
    pg.image.load(os.path.join("Assets\Images", "pacman_close_R.png")),
    (673 / 20, 721 / 20),
).convert_alpha()
pellet_image = pg.image.load(os.path.join("Assets\Images", "pellet.png")).convert_alpha()
pacman_init_image = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets\Images", "pacman.png")), (637 / 10, 721 / 10)
    ),
    180,
).convert_alpha()
pacman_init_close = pg.transform.rotate(
    pg.transform.scale(
        pg.image.load(os.path.join("Assets\Images", "pacman_close.png")),
        (637 / 10, 721 / 10),
    ),
    180,
).convert_alpha()

# num_pel_row_column = 7
num_row, num_col = 7, 7
start_num_row, start_num_col = 3,5

pacman_group = pg.sprite.GroupSingle()
current_display = pg.sprite.GroupSingle()
multiple_displays = pg.sprite.Group()
pellet_group = pg.sprite.Group()
visible_obstacles = pg.sprite.Group()
visible_obstacles_2 = pg.sprite.Group()
ghosts_group = pg.sprite.Group()
start_menu_frames = pg.sprite.Group()
menu_display = pg.sprite.Group()

walls_type = dict(
    vertical=(3, ((HEIGHT - dis_level.get_height()) / num_col)+1),
    horizontal=((WIDTH / num_row)+1, 3),
    big_H=(SWIDTH, 3),
    small_H=(WIDTH, 3),
    big_V=(3, SHEIGHT),
    small_V=(3, HEIGHT),
    start_H=(SWIDTH*40/100, 3),
    start_V=(3, SHEIGHT*80/100),
    menu_V=(3, ((80*HEIGHT/100) / start_num_col)+3),
    menu_H=(((40*SWIDTH/100)/ start_num_row)+1, 3),
)

shuffle_list = (" ", " ", " ", " ", "v", "h", "v", "h")

END_MUSIC = pg.USEREVENT_DROPFILE + 314
pg.mixer.music.set_endevent(END_MUSIC)