import os
import pygame
import pygame.freetype
import configparser
import random
import logging
import logging.config
import logging_conf
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
        config.set("Playfield", "window_background_color", "slategray")
        config.set("Playfield", "window_foreground_color", "whitesmoke")
        config.add_section("Fonts")
        config.set("Fonts", "# Path to the fontfile")
        config.set("Fonts", "file", "fonts/codeman38_deluxefont/dlxfont.ttf")
        config.set("Fonts", "# Default font size")
        config.set("Fonts", "size_fraction_of_vres", "67.5")
        config.set("Fonts", "# Default font color")
        config.set("Fonts", "font_color", "black")
        config.add_section("Game_window")
        config.set("Game_window", "# Game_window title")
        config.set("Game_window", "title", "Pygtris")
        config.set("Game_window", "# Initial Playfield Window Position")
        config.set("Game_window", "horizontal", "100")
        config.set("Game_window", "vertical", "100")
        config.add_section("Technical")
        config.set("Technical", "# Framerate limit")
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
        self.playfield_window_background_color = self.config.get("Playfield", "window_background_color")
        self.playfield_window_foreground_color = self.config.get("Playfield", "window_foreground_color")
        self.font_file = Path(self.config.get("Fonts", "file"))
        self.font_fractional_size = float(self.config.get("Fonts", "size_fraction_of_vres"))
        self.font_color = self.config.get("Fonts", "font_color")
        self.window_title = self.config.get("Game_window", "title")
        self.initial_horizontal_window_position = self.config.get("Game_window", "horizontal")
        self.initial_vertical_window_position = self.config.get("Game_window", "vertical")
        self.framerate = self.config.getint("Technical", "framerate")
        self.graphics_folder = Path(self.config.get("Graphics", "folder"))
        self.playfield_tile = self.graphics_folder / Path(self.config.get("Graphics", "empty_playfield_tile"))
    def playfield_tiles_sequence(self, tile: pygame.Surface) -> tuple:
        """
        Returns a sequence of tules (tile, (x, y)).
        Created to fill the playfield with playfield tiles.
        """
        tile_width = tile.get_width()
        tile_height = tile.get_height()
        for y in range(self.playfield_window_vertical):
            for x in range(self.playfield_window_horizontal):
                yield (tile, (x * tile_width, y * tile_height))
    def run_game(self) -> None:
        pygame.init()
        # Get display resolution
        self.current_h = pygame.display.Info().current_h
        self.current_w = pygame.display.Info().current_w
        # Set dimensions of the playfield
        self.scaling = self.current_h // self.playfield_fraction_of_vres
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.initial_horizontal_window_position},{self.initial_vertical_window_position}"
        pygame.display.set_caption(self.window_title)
        # Setup playfield
        self.playfield = pygame.display.set_mode(
                (
                    self.playfield_window_horizontal * self.scaling, 
                    self.playfield_window_vertical * self.scaling
                )
            )
        self.playfield.fill((pygame.Color(self.playfield_window_background_color)))
        self.playfield_tile = pygame.image.load(str(self.playfield_tile))
        self.playfield.blits(self.playfield_tiles_sequence(self.playfield_tile))
        pygame.display.flip()
        self.dot = pygame.Surface((50,50))
        self.dot.fill(pygame.Color("white"))
        # Setup font
        self.font_size = int(self.current_h / self.font_fractional_size)
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
        logger.debug("Setting up playfield")
        logger.debug("Rendering 'Hello better World!'")
        text_rect = self.game_font.render_to(self.playfield, (40, 350), "Hello better World!", fgcolor=self.font_fgcolor)
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
                    self.playfield.fill(pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255), 0) )
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
