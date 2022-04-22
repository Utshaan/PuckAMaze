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
        self.selected_text = f"<{text}>"
        self.selected_surf = self.font.render(self.selected_text, True, color)
        self.selected_rect_uninflated = self.selected_surf.get_rect(center = center)
        self.hovering = False
        self.selected = False
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

class SettingsButton:
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
        self.selected_text = f"<{text}>"
        self.on_text = f"{self.selected_text} : ON"
        self.on_text_unselected = f"{self.text} : ON"
        self.off_text = f"{self.selected_text} : OFF"
        self.off_text_unselected = f"{self.text} : OFF"
        self.selected_on_surf = self.font.render(self.on_text, True, color)
        self.unselected_on_surf = self.font.render(self.on_text_unselected, True, color)
        self.selected_off_surf = self.font.render(self.off_text, True, color)
        self.unselected_off_surf = self.font.render(self.off_text_unselected, True, color)
        self.selected_rect_on = self.selected_on_surf.get_rect(center = center)
        self.unselected_rect_on = self.unselected_on_surf.get_rect(center = center)
        self.selected_rect_off = self.selected_off_surf.get_rect(center = center)
        self.unselected_rect_off = self.unselected_off_surf.get_rect(center = center)
        self.hovering = False
        self.selected = True
        self.pressed = False
        self.released = False

    def draw(self) -> None:
        """Draws the text of the button"""
        if self.hovering:
            if self.selected:
                screen.blit(self.selected_on_surf, self.selected_rect_on.topleft)
            else:
                screen.blit(self.selected_off_surf, self.selected_rect_off.topleft)
        else:
            if self.selected:
                screen.blit(self.unselected_on_surf, self.unselected_rect_on.topleft)
            else:
                screen.blit(self.unselected_off_surf, self.unselected_rect_off.topleft)


    def update(self) -> None:
        """Update the button"""
        self.draw()