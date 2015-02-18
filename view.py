
""" view.py: Contains the View class. """


import random

import config
from graphics import *


class View:
    
    """ The view class which handles the visual component of the application.
    """
    
    def __init__(self, pygame, master):
        """ Set up and initialise the view. Does not start the display. """
        
        self._pygame = pygame
        self._master = master
        self._display = self._pygame.display
        self._interface = None
        self._state = None
        self._cycle_colour = (200, 0, 0)
        self._white = (255, 255, 255)
    
    def start(self):
        """ Start the display. """
        
        self._screen = self._display.set_mode((640, 480))
        self._display.set_caption('PolyominOhs!')
        self._pygame.mouse.set_visible(0)
    
    def update(self):
        """ Update the screen. """
        
        # Constantly cycle through a colour
        h, s, v = rgb2hsv(self._cycle_colour)
        h += 1
        self._cycle_colour = hsv2rgb((h, s, v))
        
        if self._state == config.GS_LOADING:
            self._screen.blit(self._background, (0, 0))
        elif self._state in [config.GS_MENU, config.GS_MENU_ENTER_HIGHSCORE,
                             config.GS_MENU_HIGHSCORES, config.GS_MENU_HELP]:
            
            # Get current selections
            selected = self._interface.get_selection()
            settings = {config.MENU_LEVEL: str(self._interface.get_level()),
                        config.MENU_ORDER: str(self._interface.get_order()),
                        config.MENU_SFX: self._interface.get_sfx(),
                        config.MENU_MUSIC: self._interface.get_music()}
            
            # Background and title
            self._screen.blit(self._background, (0, 0))
            draw_text(self._screen, (120, 25), 'PolyominOhs!', 36,
                      self._cycle_colour, self._pygame, True)
            
            # Buttons
            for button in self._buttons.items():
                if button[0] == selected:
                    button[1].draw(self._screen, config.TXT_HOVER,
                                   self._pygame, self._cycle_colour)
                else:
                    button[1].draw(self._screen, config.TXT_NORMAL,
                                   self._pygame)
            
            # Radio Selections
            for radio in self._radios.items():
                if radio[0] == selected:
                    radio[1].draw(self._screen, settings[radio[0]],
                                  config.TXT_HOVER, self._cycle_colour,
                                  self._pygame)
                else:
                    radio[1].draw(self._screen, settings[radio[0]],
                                  config.TXT_NORMAL, self._cycle_colour,
                                  self._pygame)
            
            # Random polyomino
            order = self._interface.get_order()
            ominoes = self._master._ominoes[order - 1]
            n = self._interface.get_random_omino()
            shape = ominoes[0][n]
            draw_polyomino(self._screen, (400, 160), shape, 21,
                           self._cycle_colour, self._pygame)
            
            # Highscores
            if self._state == config.GS_MENU_HIGHSCORES:
                draw_border(self._highscores, self._cycle_colour, self._pygame)
                for i, highscore in enumerate(self._master.get_highscores()):
                    name, score = highscore
                    name = name.replace('_', ' ')
                    if self._interface.get_highscore_highlight() == i:
                        colour = self._cycle_colour
                    else:
                        colour = self._white
                    draw_text(self._highscores, (20, 10 + (i + 1) * 25), name,
                              10, colour, self._pygame)
                    draw_text(self._highscores, (175, 10 + (i + 1) * 25),
                              str(score), 10, colour, self._pygame)
                self._screen.blit(self._highscores, (200, 100))
            
            # Enter highscore
            if self._state == config.GS_MENU_ENTER_HIGHSCORE:
                self._enterhighscore.fill((0, 0, 0))
                draw_border(self._enterhighscore, self._cycle_colour,
                            self._pygame)
                draw_text(self._enterhighscore, (60, 20), 'Highscore!', 14,
                          self._white, self._pygame)
                draw_text(self._enterhighscore, (20, 60),
                          'Please enter your name:', 10, self._white,
                          self._pygame)
                draw_text(self._enterhighscore, (70, 170), 'Press return', 10,
                          self._white, self._pygame)
                self._name_entry.update(self._interface.get_highscore_name())
                self._name_entry.draw(self._enterhighscore,
                                      self._interface.get_name_selected(),
                                      self._cycle_colour, self._pygame)
                self._screen.blit(self._enterhighscore, (200, 120))
            
            # Help
            if self._state == config.GS_MENU_HELP:
                draw_border(self._help, self._cycle_colour, self._pygame)
                self._screen.blit(self._help, (115, 120))
            
        elif self._state in [config.GS_GAME, config.GS_GAME_PAUSED,
                             config.GS_GAME_OVER]:
            
            # Get current information
            score = str(self._interface.get_score())
            lines = str(self._interface.get_lines_cleared())
            next_omino = self._interface.get_next_omino()
            
            self._screen.blit(self._background, (0, 0))
            
            # Score and number of lines cleared
            draw_text(self._screen, (445, 155), score, 10, self._white,
                      self._pygame)
            draw_text(self._screen, (445, 215), lines, 10, self._white,
                      self._pygame)
            
            # Draw next polyomino
            if self._state == config.GS_GAME:
                draw_polyomino(self._screen, (440, 290), next_omino.get_shape(0),
                               21, next_omino.get_colour(), self._pygame)
            
            # Draw grid of blocks (or pause or game over screen)
            grid = self._interface.get_field().get_complete_grid()
            self._grid.fill((0, 0, 0))
            draw_border(self._grid, self._cycle_colour, self._pygame)
            
            if self._state == config.GS_GAME:
                size = config.sizes[self._interface.get_order()]
                draw_grid(self._grid, (5, 5), grid, size, self._pygame)
            elif self._state == config.GS_GAME_PAUSED:
                draw_text(self._grid, (30, 115), 'Game Paused', 14,
                          self._cycle_colour, self._pygame, True)
                draw_text(self._grid, (40, 185), 'Press y to quit', 10,
                          self._white, self._pygame)
                draw_text(self._grid, (30, 215), 'or esc to resume', 10,
                          self._white, self._pygame)
            elif self._state == config.GS_GAME_OVER:
                draw_text(self._grid, (42, 115), 'Game Over', 14,
                          self._cycle_colour, self._pygame, True)
                draw_text(self._grid, (47, 185), 'Press return', 10,
                          self._white, self._pygame)
            
            self._screen.blit(self._grid, (60, 30))
        
        self._display.flip()
    
    def change_state(self, state, interface=None):
        """ Change the state of the application and get the new interface
        (if given). Set up graphics for the new state if required.
        
        change_state(int, Menu/Game) -> void
        """
        
        self._state = state
        if interface != None:
            self._interface = interface
        
        if self._state == config.GS_LOADING:
            
            # Background with loading text
            self._background = self._pygame.Surface(self._screen.get_size())
            self._background = self._background.convert()
            self._background.fill((0, 0, 0))
            draw_text(self._background, (180, 180), 'Loading...', 36,
                      self._white, self._pygame)
        
        elif self._state == config.GS_GAME:
            
            # Background with static text
            self._background = self._pygame.Surface(self._screen.get_size())
            self._background = self._background.convert()
            self._background.fill((0, 0, 0))
            
            draw_text(self._background, (410, 130), 'Score:', 10,
                      self._white, self._pygame)
            draw_text(self._background, (410, 190), 'Lines Cleared:', 10,
                      self._white, self._pygame)
            
            next_text = 'Next ' + \
                        config.names[self._interface.get_order()].title() + ':'
            draw_text(self._background, (410, 250), next_text, 10,
                      self._white, self._pygame)
            
            # Grid
            w = 210 + 10 - self._interface.get_field().get_size()[0] + 1
            h = 420 + 10 - self._interface.get_field().get_size()[1] + 1
            self._grid = self._pygame.Surface((w, h))
            self._grid = self._grid.convert()
            self._grid.fill((0, 0, 0))
            self._grid.set_colorkey((0, 0, 0))
            
        elif self._state in [config.GS_MENU, config.GS_MENU_ENTER_HIGHSCORE,
                             config.GS_MENU_HIGHSCORES]:
            
            # Background with static text
            self._background = self._pygame.Surface(self._screen.get_size())
            self._background = self._background.convert()
            self._background.fill((0, 0, 0))
            
            draw_text(self._background, (110, 300), 'Settings:', 10,
                      self._white, self._pygame)
            draw_text(self._background, (130, 340), 'Difficulty Level:', 10,
                      self._white, self._pygame)
            draw_text(self._background, (130, 400), 'Polyomino Order:', 10,
                      self._white, self._pygame)
            
            draw_text(self._background, (370, 300), 'Audio:', 10,
                      self._white, self._pygame)
            draw_text(self._background, (400, 340), 'Sound Effects:', 10,
                      self._white, self._pygame)
            draw_text(self._background, (400, 400), 'Music:', 10,
                      self._white, self._pygame)
            
            # Buttons
            self._buttons = {}
            start_game_button = Button('Start Game', 10, (90, 150))
            self._buttons.update({config.MENU_START: start_game_button})
            view_highscores_button = Button('View Highscores', 10, (90, 180))
            self._buttons.update({config.MENU_HIGHSCORES: view_highscores_button})
            help_button = Button('Help', 10, (90, 210))
            self._buttons.update({config.MENU_HELP: help_button})
            quit_button = Button('Quit', 10, (90, 240))
            self._buttons.update({config.MENU_QUIT: quit_button})
            
            # Radio Selections
            self._radios = {}
            level_selection = Radio_Selection([str(n + 1) for n in range(9)],
                                              10, (160, 365))
            self._radios.update({config.MENU_LEVEL: level_selection})
            order_selection = Radio_Selection([str(n + 1) for n in range(6)],
                                              10, (160, 425))
            self._radios.update({config.MENU_ORDER: order_selection})
            sfx_selection = Radio_Selection(['On', 'Off'], 10, (435, 365))
            self._radios.update({config.MENU_SFX: sfx_selection})
            music_selection = Radio_Selection(['On', 'Off'], 10, (435, 425))
            self._radios.update({config.MENU_MUSIC: music_selection})
            
            # Highscores Screen
            self._highscores = self._pygame.Surface((250, 300))
            self._highscores = self._highscores.convert()
            self._highscores.fill((0, 0, 0))
            
            draw_text(self._highscores, (15, 10), 'Highscores:', 10,
                      self._white, self._pygame)
            
            # Enter highscore name screen
            self._enterhighscore = self._pygame.Surface((250, 210))
            self._enterhighscore = self._enterhighscore.convert()
            self._enterhighscore.fill((0, 0, 0))
            self._name_entry = Text_Entry(3, ['A', 'A', 'A'], 20, (85, 105))
            
            # Help Screen
            self._help = self._pygame.Surface((410, 240))
            self._help = self._help.convert()
            self._help.fill((0, 0, 0))
            
            draw_text(self._help, (15, 10), 'Controls:', 10, self._white,
                      self._pygame)
            draw_text(self._help, (205, 10), 'Instructions:', 10,
                      self._white, self._pygame)
            
            draw_text(self._help, (20, 45), 'Up - Rotate', 10, self._white,
                      self._pygame)
            draw_text(self._help, (20, 75), 'Left - Move Left', 10,
                      self._white, self._pygame)
            draw_text(self._help, (20, 105), 'Right - Move Right', 10,
                      self._white, self._pygame)
            draw_text(self._help, (20, 135), 'Down - Move Down', 10,
                      self._white, self._pygame)
            draw_text(self._help, (20, 165), 'Space - Drop', 10, self._white,
                      self._pygame)
            draw_text(self._help, (20, 195), 'Esc - Pause', 10, self._white,
                      self._pygame)
            
            text = config.instructions
            rect = self._pygame.Rect(0, 0, 190, 190)
            instructions = render_textrect(text, 8, rect, self._white,
                                           (0, 0, 0), 0, self._pygame)
            self._help.blit(instructions, (210, 45))
            