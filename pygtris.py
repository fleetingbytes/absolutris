import os
import pygame
import pygame.freetype
import configparser
import random
from pathlib import Path

def read_or_create_config_file(path_to_configfile):
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
        config.set("Playfield", "window_vertical", "22")
        config.set("Playfield", "fraction_of_vres", "27")
        config.set("Playfield", "window_background_color", "slategray")
        config.set("Playfield", "window_foreground_color", "whitesmoke")
        config.add_section("Fonts")
        config.set("Fonts", "# Path to the fontfile")
        config.set("Fonts", "file", "fonts/codeman38_deluxefont/dlxfont.ttf")
        config.set("Fonts", "# Default font size")
        config.set("Fonts", "size_fraction_of_vres", "67.5")
        config.set("Fonts", "# Default font color")
        config.set("Fonts", "font_color", "black")
        config.add_section("Initial_Window_Position")
        config.set("Initial_Window_Position", "# Initial Playfield Window Position")
        config.set("Initial_Window_Position", "horizontal", "100")
        config.set("Initial_Window_Position", "vertical", "100")
        config.add_section("Technical")
        config.set("Technical", "# Framerate limit")
        config.set("Technical", "framerate", "100")
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
        # Get display resolution
        self.current_h = pygame.display.Info().current_h
        self.current_w = pygame.display.Info().current_w
        # Set dimensions of the playfield
        self.scaling = self.current_h // int(self.config.get("Playfield", "fraction_of_vres"))
        self.init_h_pos = self.config.getint("Initial_Window_Position", "horizontal")
        self.init_v_pos = self.config.getint("Initial_Window_Position", "vertical")
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.init_h_pos},{self.init_v_pos}"
        # wh = self.config.getint("Playfield", "window_horizontal")
        # wv = self.config.getint("Playfield", "window_vertical")
        self.playfield = pygame.display.set_mode(
                (
                    # wh * self.scaling,
                    # wv * self.scaling
                    self.config.getint("Playfield", "window_horizontal") * self.scaling, 
                    self.config.getint("Playfield", "window_vertical") * self.scaling
                )
            )
        self.playfield.fill((pygame.Color(self.config.get("Playfield", "window_background_color"))))
        pygame.display.flip()
        # self.playfield_surface = pygame.Surface((wh, wv))
        self.dot = pygame.Surface((50,50))
        self.dot.fill(pygame.Color("white"))
        # Setup font
        self.font_size = int(self.current_h / float(self.config.get("Fonts", "size_fraction_of_vres")))
        self.game_font = pygame.freetype.Font(
                self.config.get("Fonts", "file"), 
                self.font_size
            )
        pygame.freetype.Font.fgcolor = pygame.Color(self.config.get("Fonts", "font_color"))
        # Setup game clock
        self.clock = pygame.time.Clock()
        # Setup events
        self.CHANGE_COLOR_EVENT = pygame.USEREVENT
        # Setup timers
        pygame.time.set_timer(self.CHANGE_COLOR_EVENT, 1000)
        # Main game loop
        self.pygame_running = True
        while self.pygame_running:
            self.clock.tick(self.config.getint("Technical", "framerate"))
            list_of_rectangles_to_update = list()
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
                        list_of_rectangles_to_update.append(self.playfield.blit(self.dot, (60, 400)))
                if event.type == self.CHANGE_COLOR_EVENT:
                    self.playfield.fill(pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255), 0) )
            text_rect = (self.game_font.render_to(self.playfield, (40, 350), "Hello better World!"))
            text_rect = pygame.Rect(40, 350, text_rect.w, text_rect.h)
            list_of_rectangles_to_update.append(text_rect)
            pygame.display.update(list_of_rectangles_to_update)
        pygame.quit()


if __name__ == "__main__":
    configfilepath = Path("config.ini")
    debug_delete_config(configfilepath)
    game = Game(configfilepath)
    game.run_game()
