#!/usr/bin/env python

import dataclasses
import pygame


@dataclasses.dataclass
class Gui:
    """
    Class for GUIs of Absolutris.
    """
    game_window_x_pos: int = 24
    game_window_y_pos: int = 36
    game_window_title: str = "Absolutris"
    game_window_width: int = 1920-24*2
    game_window_height: int = 1080-24*4
    flags: int = 0
    colors_window_bg: pygame.Color = pygame.Color(18, 18, 18, 255)
    colors_window_fg: pygame.Color = pygame.Color(245, 245, 245, 255)
    colors_font_fg: pygame.Color = pygame.Color(70, 70, 70, 255)
    playfield_width: int = 10
    playfield_height: int = 20
    pixel_width: int = 3
    pixel_height: int = 3
    mino_width: int = 8
    mino_height: int = 8


class Malicious(Gui):
    pass


default = Gui()
debug = Gui(flags=32)

m = Malicious(
        game_window_x_pos=0,
        game_window_y_pos=0,
        game_window_width=7680,
        game_window_height=4320,
        flags=pygame.NOFRAME,
        playfield_width=4,
        pixel_width=1,
        mino_width=1,
        playfield_height=4,
        pixel_height=1,
        mino_height=1,
        )


if __name__ == "__main__":
    pass
