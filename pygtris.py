import os
import pygame
import pygame.freetype
import configparser
import random
import logging
import logging.config
import logging_conf
import numpy as np
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
        config.set("Playfield", "window_horizontal", "10")
        config.set("Playfield", "window_vertical", "24")
        config.set("Playfield", "fraction_of_vres", "30")
        config.set("Playfield", "x_position", "300")
        config.set("Playfield", "y_position", "60")
        config.add_section("Fonts")
        config.set("Fonts", "# Path to the fontfile")
        config.set("Fonts", "file", "fonts/codeman38_deluxefont/dlxfont.ttf")
        config.set("Fonts", "# Default font size")
        config.set("Fonts", "size_fraction_of_vres", "67.5")
        config.set("Fonts", "# Default font color")
        config.set("Fonts", "font_color", "black")
        config.add_section("Game_window")
        config.set("Game_window", "# Game Window Title")
        config.set("Game_window", "title", "Pygtris")
        config.set("Game_window", "# Initial Game Window Position")
        config.set("Game_window", "horizontal", "0")
        config.set("Game_window", "vertical", "0")
        config.set("Game_window", "# Game Window Size")
        config.set("Game_window", "width", "1920")
        config.set("Game_window", "height", "1080")
        config.set("Game_window", "background_color", "slategray")
        config.set("Game_window", "foreground_color", "whitesmoke")
        config.add_section("Technical")
        config.set("Technical", "# Framerate Limit")
        config.set("Technical", "framerate", "100")
        config.add_section("Graphics")
        config.set("Graphics", "folder", "img")
        config.set("Graphics", "empty_playfield_tile", "playfield_tile.png")
        with open(path_to_configfile, mode="w", encoding="utf-8") as configfh:
            config.write(configfh)
    config.read(path_to_configfile)
    return config


def debug_delete_config(path_to_configfile: Path) -> None:
    """
    Serves debugging purposes. Deletes the config file.
    """
    if path_to_configfile.is_file():
        path_to_configfile.unlink()


class Tile():
    def __init__(self, hold: pygame.Surface) -> None:
        self.hold = [hold]


class Playfield():
    def __init__(self, x_dim: int, y_dim: int, x_pos: int, y_pos: int, sequence) -> None:
        self.playfield = np.asarray(sequence, dtype=object).reshape(y_dim, x_dim)
        self.x_pos = x_pos
        self.y_pos = y_pos
    def serialize(self) -> tuple:
        """
        Returns a sequence of tiles (tile: pygame.Surface, (x, y)).
        Created to fill the blits method of playfield surface.
        """
        tile_width = self.playfield[0, 0].hold[-1].get_width()
        tile_height = self.playfield[0, 0].hold[-1].get_height()
        rows = self.playfield.shape[0]
        columns = self.playfield.shape[1]
        for y in range(rows):
            for x in range(columns):
                yield (self.playfield[y, x].hold[-1], (x * tile_width + self.x_pos, y * tile_height + self.y_pos))

class Game():
    """
    A class to run the game
    """
    def __init__(self, path_to_configfile: Path) -> None:
        self.config = read_or_create_config_file(path_to_configfile)
        self.load_config()
    def load_config(self) -> None:
        self.playfield_window_horizontal = self.config.getint("Playfield", "window_horizontal")
        self.playfield_window_vertical = self.config.getint("Playfield", "window_vertical")
        self.playfield_fraction_of_vres = int(self.config.getint("Playfield", "fraction_of_vres"))
        self.playfield_x_position = int(self.config.getint("Playfield", "x_position"))
        self.playfield_y_position = int(self.config.getint("Playfield", "y_position"))
        self.font_file = Path(self.config.get("Fonts", "file"))
        self.font_size_fraction_of_vres = float(self.config.get("Fonts", "size_fraction_of_vres"))
        self.font_color = self.config.get("Fonts", "font_color")
        self.window_title = self.config.get("Game_window", "title")
        self.initial_horizontal_window_position = self.config.get("Game_window", "horizontal")
        self.initial_vertical_window_position = self.config.get("Game_window", "vertical")
        self.game_window_width = self.config.getint("Game_window", "width")
        self.game_window_height = self.config.getint("Game_window", "height")
        self.game_window_background_color = self.config.get("Game_window", "background_color")
        self.game_window_foreground_color = self.config.get("Game_window", "foreground_color")
        self.framerate = self.config.getint("Technical", "framerate")
        self.graphics_folder = Path(self.config.get("Graphics", "folder"))
        self.playfield_tile_img = self.graphics_folder / Path(self.config.get("Graphics", "empty_playfield_tile"))
    def setup_game_window(self) -> None:
        self.game_window = pygame.display.set_mode(
                (
                    self.game_window_width,
                    self.game_window_height
                ),
                pygame.NOFRAME
            )
        self.game_window.fill((pygame.Color(self.game_window_background_color)))
    def setup_UI_playfield(self) -> None:
        """
        UI playfield is the area where user sees the tetrominoes falling.
        UI playfield includes the 10x2 spawn area where tetrominoes spawn.
        UI playfield includes the 10x2 reserved area above the spawn needed
        to rotate tetrominoes in their spawn area before their first fall step.

        This function renders the empty UI playfield when the game is started.
        It fills it with empty playfield tile images.
        """
        # Setup UI playfield
        logger.debug("Setting up UI playfield")
        # load tile image
        tile_image = pygame.image.load(str(self.playfield_tile_img))
        ## Create a sequence of 240 empty tiles
        tile_sequence = [Tile(tile_image) for x in range(self.playfield_window_horizontal * self.playfield_window_vertical)]
        ## Use this sequence to construct an empty playfield
        self.pf = Playfield(self.playfield_window_horizontal, 
                            self.playfield_window_vertical, 
                            self.playfield_x_position, 
                            self.playfield_y_position, 
                            tile_sequence)
        self.game_window.blits(self.pf.serialize())
        pygame.display.flip()
    def run_game(self) -> None:
        # Set initial game window position
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.initial_horizontal_window_position},{self.initial_vertical_window_position}"
        pygame.init()
        # Get monitor's resolution
        self.current_display_vres = pygame.display.Info().current_h
        self.current_display_hres = pygame.display.Info().current_w
        # Find out how to scale the game window
        logger.warning("Need to find out how to scale the game window.")
        self.setup_game_window()
        # Render the UI playfield
        self.setup_UI_playfield()
        pygame.display.set_caption(self.window_title)
        # Square dot to display after a key press (testing key input)
        self.dot = pygame.Surface((50,50))
        self.dot.fill(pygame.Color("white"))
        # Setup font
        self.font_size = int(self.current_display_vres / self.font_size_fraction_of_vres)
        self.game_font = pygame.freetype.Font(
                str(self.font_file), 
                self.font_size
            )
        self.font_fgcolor = pygame.Color(self.font_color)
        # Setup game clock
        self.clock = pygame.time.Clock()
        # Setup events
        self.TICK = pygame.USEREVENT + 0
        self.DROPSTEP = pygame.USEREVENT + 1
        # Generate a TICK event every 1000 milliseconds
        pygame.time.set_timer(self.TICK, 1000)
        # Prepare list of rectangles to update
        self.list_of_rectangles_to_update = list()
        # Start the game
        self.pygame_running = True
        logger.info("Starting game")
        logger.debug("Rendering 'Hello better World!'")
        text_rect = self.game_font.render_to(self.game_window, (40, 350), "Hello better World!", fgcolor=self.font_fgcolor)
        logger.debug("Moving it into position")
        text_rect = pygame.Rect(40, 350, text_rect.w, text_rect.h)
        self.list_of_rectangles_to_update.append(text_rect)
        # Main game loop
        while self.pygame_running:
            pygame.display.update(self.list_of_rectangles_to_update)
            self.clock.tick(self.framerate)
            self.list_of_rectangles_to_update = list()
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
                        self.list_of_rectangles_to_update.append(self.playfield.blit(self.dot, (60, 400)))
                if event.type == self.TICK:
                    self.game_window.fill(pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255), 0) )
                    self.list_of_rectangles_to_update.append(text_rect)
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
