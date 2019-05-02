import pygame
import pygame.freetype
import configparser
from pathlib import Path


def read_or_create_config_file(path_to_configfile):
    """
    Creates config file with default values
    or reads the current config file "config.ini".
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    if not path_to_configfile.is_file():
        config.add_section("Display")
        config.set("Display", "# Settings related to the program window")
        config.set("Display", "window_horizontal", "800")
        config.set("Display", "window_vertical", "600")
        config.set("Display", "window_background_color", "chocolate")
        config.add_section("Fonts")
        config.set("Fonts", "# Path to the fontfile")
        config.set("Fonts", "file", "fonts/codeman38_deluxefont/dlxfont.ttf")
        config.set("Fonts", "# Default font size")
        config.set("Fonts", "size", "16")
        config.set("Fonts", "# Default font color")
        config.set("Fonts", "font_color", "black")
        with open(path_to_configfile, mode="w", encoding="utf-8") as configfh:
            config.write(configfh)
    config.read(path_to_configfile)
    return config


def debug_delete_config(path_to_configfile):
    """
    Serves debugging purposes. Deletes the config file.
    """
    if path_to_configfile.is_file():
        path_to_configfile.unlink()


class Game():
    """
    A class to run the game
    """
    def __init__(self, path_to_configfile):
        self.config = read_or_create_config_file(path_to_configfile)
    def run_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
                (
                    self.config.getint("Display", "window_horizontal"), 
                    self.config.getint("Display", "window_vertical")
                )
            )
        self.game_font = pygame.freetype.Font(
                self.config.get("Fonts", "file"), 
                self.config.getint("Fonts", "size")
            )
        self.pygame_window_opened = True
        while self.pygame_window_opened:
            for event in pygame.event.get():
                # Assume main game window is closed when pygame is quitting
                if event.type == pygame.QUIT:
                    self.pygame_window_opened = False
                # Close main window if Ctrl+Q is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_CTRL:
                            self.pygame_window_opened = False
                        continue
            self.screen.fill((pygame.Color(self.config.get("Display", "window_background_color"))))
            text_surface, _ = self.game_font.render("Hello World!", (pygame.Color(self.config.get("Fonts", "font_color"))))
            self.screen.blit(text_surface, (40, 250))
            self.game_font.render_to(self.screen, (40, 350), "Hello better World!", pygame.Color(self.config.get("Fonts", "font_color")))
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    configfilepath = Path("config.ini")
    debug_delete_config(configfilepath)
    game = Game(configfilepath)
    game.run_game()
