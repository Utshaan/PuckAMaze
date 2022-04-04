from screen import SWIDTH, SHEIGHT, pg, screen, InGame_FONT

class Button:
    def __init__(
        self,
        text: str,
        center: tuple[int, int] = (SWIDTH // 2, SHEIGHT // 2),
        font: pg.font.Font = InGame_FONT,
        color="lightgray",
    ) -> None:
        """Initialize a new button
        Args:
            text : Text to show on button.
            center : Coordinates of center of the button. Defaults to center of screen).
            font : Font for the text on the button. Defaults to pg.font.Font("fonts/Roboto-Black.ttf", 32).
            color : Color of the text on the button. Defaults to light gray.
        """
        self.text = text
        self.font = font
        self.image = self.font.render(self.text, True, color)
        self.image_rect = self.image.get_rect(center=center)
        self.selected = f"<{text}>"
        self.selected_surf = self.font.render(self.selected, True, color)
        self.selected_rect_uninflated = self.selected_surf.get_rect(center = center)
        self.hovering = False
        self.pressed = False
        self.released = False

    def draw(self) -> None:
        """Draws the text of the button"""
        if self.hovering:
            screen.blit(self.selected_surf, self.selected_rect_uninflated.topleft)
        else:
            screen.blit(self.image, self.image_rect.topleft)

    def update(self) -> None:
        """Update the button"""
        self.draw()
