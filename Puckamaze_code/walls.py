from screen import colours, walls_type ,pg

class Walls(pg.sprite.Sprite):
    def __init__(
        self, w_type: str, pos: tuple, colour: str = "dark_teal", *group: list
    ) -> None:
        """Creates Walls

        Args:
            w_type (str): an entry from walls_type dict
            pos(tuple): coordinates
            *group (list): a group
            colour (str, optional): an entry from colours dict. Defaults to 'dark_teal'.
        """
        super().__init__(*group)
        self.image = pg.Surface(walls_type[w_type])
        self.image.fill(colours[colour])
        self.rect = self.image.get_rect(topleft=pos)