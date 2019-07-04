import os
import pygame
import pygame.freetype
import configparser
import random
import logging
import logging.config
import logging_conf
import numpy as np
from typing import Iterator
from pathlib import Path

# Setup logging
logging.config.dictConfig(logging_conf.dict_config)
logger = logging.getLogger()

def read_or_create_config_file(path_to_configfile: Path) -> configparser.ConfigParser:
    """
    Creates config file with default values
    or reads the current config file "config.ini".
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    if not path_to_configfile.is_file():
        config.add_section("Playfield")
        config.set("Playfield", "# Settings related to the playfield window")
        config.set("Playfield", "columns", "10")
        config.set("Playfield", "rows", "24")
        config.set("Playfield", "fraction_of_vres", "30")
        config.set("Playfield", "x_position", "26")
        config.set("Playfield", "y_position", "3")
        config.add_section("Fonts")
        config.set("Fonts", "# Path to the fontfile")
        config.set("Fonts", "file", "fonts/codeman38_deluxefont/dlxfont.ttf")
        config.set("Fonts", "# Default font size")
        config.set("Fonts", "size_fraction_of_vres", "67.5")
        config.add_section("Game_window")
        config.set("Game_window", "# Game Window Title")
        config.set("Game_window", "title", "Pygtris")
        config.set("Game_window", "# Initial Game Window Position")
        config.set("Game_window", "horizontal", "0")
        config.set("Game_window", "vertical", "0")
        config.set("Game_window", "# Game Window Size")
        config.set("Game_window", "width", "1920")
        config.set("Game_window", "height", "1080")
        config.add_section("Technical")
        config.set("Technical", "# Framerate Limit")
        config.set("Technical", "framerate", "100")
        config.add_section("Graphics")
        config.set("Graphics", "folder", "img")
        config.set("Graphics", "empty_playfield_tile", "playfield_tile.png")
        config.add_section("Colors")
        config.set("Colors", "# Color values need to be separated by comma and space \", \"")
        config.set("Colors", "game_window_background_color", "18, 18, 18, 255")
        config.set("Colors", "game_window_foreground_color", "245, 245, 245, 255")
        config.set("Colors", "font_color", "70, 70, 70, 255")
        with open(path_to_configfile, mode="w", encoding="utf-8") as configfh:
            config.write(configfh)
    config.read(path_to_configfile)
    return config


def debug_delete_config(path_to_configfile: Path) -> None:
    """
    Serves debugging purposes. Deletes the config file.
    """
    logger.debug("Deleting config file")
    if path_to_configfile.is_file():
        path_to_configfile.unlink()


class Tile():
    def __init__(self, surface: pygame.Surface) -> None:
        """
        Creates a Tile which is a direct subsurface of the game window.
        """
        self.surface = surface
        self.hold = []


class Playfield():
    def __init__(self, x_dim: int, y_dim: int, sequence: Iterator[Tile], img: pygame.Surface, rects_to_update: list) -> None:
        self.tile_array = np.asarray(list(sequence), dtype=object).reshape(y_dim, x_dim)
        self.rects_to_update = rects_to_update
        self.blit_initial_images(img)
    def blit_initial_images(self, img) -> None:
        rows, columns = self.tile_array.shape
        for row in range(rows):
            for column in range(columns):
                self.tile_array[row, column].surface.blit(img, (0, 0))
    def blit(self, x: int, y: int, srf: pygame.Surface) -> None:
        tile = self.tile_array[x, y].surface
        rect = tile.blit(srf, (0, 0))
        self.rects_to_update.append(rect.move(tile.get_abs_offset()))


class Game():
    """
    A class to run the game
    """
    def __init__(self, path_to_configfile: Path) -> None:
        self.config = read_or_create_config_file(path_to_configfile)
        self.config.getcolor = self.get_color
        self.load_config()
    def get_color(self, section, key):
        """
        This function helps to retrieve the color values from the config file
        """
        return pygame.Color(*[int(x) for x in self.config.get(section, key).split(", ")])
    def load_config(self) -> None:
        self.playfield_columns = self.config.getint("Playfield", "columns")
        self.playfield_rows = self.config.getint("Playfield", "rows")
        self.playfield_fraction_of_vres = int(self.config.getint("Playfield", "fraction_of_vres"))
        self.playfield_x_position = self.config.getint("Playfield", "x_position")
        self.playfield_y_position = self.config.getint("Playfield", "y_position")
        self.font_file = Path(self.config.get("Fonts", "file"))
        self.font_size_fraction_of_vres = float(self.config.get("Fonts", "size_fraction_of_vres"))
        self.window_title = self.config.get("Game_window", "title")
        self.initial_horizontal_window_position = self.config.get("Game_window", "horizontal")
        self.initial_vertical_window_position = self.config.get("Game_window", "vertical")
        self.game_window_width = self.config.getint("Game_window", "width")
        self.game_window_height = self.config.getint("Game_window", "height")
        self.framerate = self.config.getint("Technical", "framerate")
        self.graphics_folder = Path(self.config.get("Graphics", "folder"))
        self.playfield_tile_file = self.graphics_folder / Path(self.config.get("Graphics", "empty_playfield_tile"))
        self.game_window_background_color = self.config.getcolor("Colors", "game_window_background_color")
        self.game_window_foreground_color = self.config.getcolor("Colors", "game_window_foreground_color")
        self.font_color = self.config.getcolor("Colors", "font_color")
    def create_playfield_tiles(self) -> Iterator[Tile]:
        for y in range(self.playfield_rows):
            for x in range(self.playfield_columns):
                rect = pygame.Rect(x * self.playfield_tile_img.get_width() + self.playfield_x_position * self.playfield_fraction_of_vres, 
                                   y * self.playfield_tile_img.get_height() + self.playfield_y_position * self.playfield_fraction_of_vres, 
                                   self.playfield_tile_img.get_width(), 
                                   self.playfield_tile_img.get_height())
                yield Tile(self.game_window.subsurface(rect))
    def setup_game_window(self) -> None:
        pygame.display.set_caption(self.window_title)
        self.game_window = pygame.display.set_mode(
                (
                    self.game_window_width,
                    self.game_window_height
                ),
                pygame.NOFRAME
            )
        self.game_window.fill((self.game_window_background_color))
        # load tile image
        self.playfield_tile_img = pygame.image.load(str(self.playfield_tile_file))
        # Create tiles of the playfield and blit their empty tile images
        self.pf = Playfield(self.playfield_columns, self.playfield_rows, self.create_playfield_tiles(), self.playfield_tile_img, self.list_of_rectangles_to_update)
    def run_game(self) -> None:
        # Set initial game window position
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.initial_horizontal_window_position},{self.initial_vertical_window_position}"
        pygame.init()
        # Get monitor's resolution
        self.current_display_vres = pygame.display.Info().current_h
        self.current_display_hres = pygame.display.Info().current_w
        self.playfield_x_dim = self.current_display_vres / self.playfield_fraction_of_vres * self.playfield_columns
        self.playfield_y_dim = self.current_display_vres / self.playfield_fraction_of_vres * self.playfield_rows
        # Prepare list of rectangles to update
        self.list_of_rectangles_to_update = list()
        # Find out how to scale the game window
        logger.warning("Need to find out how to scale the game window.")
        self.setup_game_window()
        pygame.display.flip()
        # Square dot to display after a key press (testing key input)
        self.dot = pygame.Surface((50,50))
        self.dot.fill(pygame.Color("white"))
        # Setup font
        self.font_size = int(self.current_display_vres / self.font_size_fraction_of_vres)
        self.game_font = pygame.freetype.Font(
                str(self.font_file), 
                self.font_size
            )
        # Setup game clock
        self.clock = pygame.time.Clock()
        # Setup events
        self.TICK = pygame.USEREVENT + 0
        self.DROPSTEP = pygame.USEREVENT + 1
        # Generate a TICK event every 1000 milliseconds
        pygame.time.set_timer(self.TICK, 1000)
        # Start the game
        self.pygame_running = True
        logger.info("Starting game")
        logger.debug("Rendering 'Hello better World!'")
        text_rect = self.game_font.render_to(self.game_window, (40, 350), "Hello better World!", fgcolor=self.font_color)
        logger.debug("Moving it into position")
        text_rect = pygame.Rect(40, 350, text_rect.w, text_rect.h)
        self.list_of_rectangles_to_update.append(text_rect)
        # Main game loop
        while self.pygame_running:
            pygame.display.update(self.list_of_rectangles_to_update)
            self.clock.tick(self.framerate)
            # Need to clear the list carefully, because it is shared among instances of classes
            for _ in range(len(self.list_of_rectangles_to_update)):
                del self.list_of_rectangles_to_update[0]
            for event in pygame.event.get():
                # When user closes window with the mouse
                if event.type == pygame.QUIT:
                    self.pygame_running = False
                    break
                # Close main window if Ctrl+Q is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_CTRL:
                            self.pygame_running = False
                        break
                    if event.key == pygame.K_y:
                        brick = pygame.image.load("img/brick.png")
                        tile = self.pf.tile_array[0, 0].surface
                        rect = tile.blit(brick, (0, 0))
                        abs_offset = tile.get_abs_offset()
                        moved_rect = rect.move(abs_offset)
                        self.list_of_rectangles_to_update.append(moved_rect)
                    if event.key == pygame.K_k:
                        # try new function
                        self.pf.blit(4, 7, pygame.image.load("img/brick.png"))
                if event.type == self.TICK:
                    # self.game_window.fill(pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255), 0) )
                    # self.list_of_rectangles_to_update.append(text_rect)
                    logger.debug(f"TICK with {len(self.list_of_rectangles_to_update)} rects to redraw")
        logger.info("Quitting game")
        pygame.quit()


if __name__ == "__main__":
    configfilepath = Path("config.ini")
    debug_delete_config(configfilepath)
    game = Game(configfilepath)
    try:
        game.run_game()
    except Exception as err:
        logger.exception(f"{err.args[0]} occurred")
