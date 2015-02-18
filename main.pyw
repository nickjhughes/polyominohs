
""" main.py: The main entry point into the application, and contains the main
Polyominohs class. """


import sys

try:
    import pygame
except ImportError:
    print 'This application requires the pygame library to be installed.', \
           'The application will now close.'
    sys.exit(-1)

import config
from event_handler import *
from sound import *
from view import *
from menu import *
from game import *


class Polyominohs:
    
    """ The main game class which controls the application at the highest
    level, as well as taking care of file handling (ie. high scores file). """
    
    def __init__(self):
        """ Initalise instances of the main classes, load high scores list
        and set up anything else needed. """
        
        self._pygame = pygame
        if not ((self._pygame.init()[0] == 5 and
           self._pygame.mixer.get_init() == None) or
           self._pygame.init()[0] == 6):
            # We can deal with no sound, but need everything else
            print 'Not all required pygame modules could be initialised.', \
                  'The application will now close.'
            sys.exit(-1)
        self._events = Event_Handler(self._pygame)
        self._sound = Sound(self._pygame)
        self._view = View(self._pygame, self)
        self._load_highscores()
        self._state = config.GS_LOADING
        self._menu = None
        self._game = None
    
    def run(self):
        """ Start the game and continue until the user quits. """
        
        self._view.start()
        self.change_state(config.GS_LOADING)
        self._view.update()
        
        # Generate all polyominoes while the user sees a loading screen
        generator = Generator()
        self._ominoes = []
        for order in xrange(6):
            shapes = generator.generate(order + 1)
            colours = generator.generate_colours(len(shapes))
            self._ominoes.append((shapes, colours))
        
        level = 1
        order = 4
        is_highscore = False
        while True:
            self._menu = Menu(self, self._view, self._events, self._sound,
                              level, order)
            if is_highscore:
                self.change_state(config.GS_MENU_ENTER_HIGHSCORE)
                self._menu.highscore = score
            else:
                self.change_state(config.GS_MENU)
            order, level = self._menu.loop()
            if order == 0:
                self._pygame.quit()
                return
            self.change_state(config.GS_LOADING)
            self._view.update()
            self._game = Game(self, self._view, self._events, self._sound,
                              level, order, self._ominoes[order - 1])
            self.change_state(config.GS_GAME)
            score = self._game.loop()
            if score == None:
                self._pygame.quit()
                return
            is_highscore = self._is_highscore(score)
            self._game = None
            self._menu = None
    
    def get_state(self):
        """ Return the state of the application.
        
        get_state() -> int
        """
        
        return self._state
        
    def get_highscores(self):
        """ Return the list of highscores as pairs of (name, score).
        
        get_highscores() -> list<(string, int)>
        """
        
        return self._highscores
    
    def change_state(self, state):
        """ Change the state of the application and inform all the other
        main game objects of the new state.
        
        change_state(int) -> void
        Precondition: The interface for the given state has been set.
        """
        
        old_state = self._state
        self._state = state
        
        new_interface = None
        if old_state in config.GAME_STATES and state in config.MENU_STATES:
            new_interface = self._menu
        elif old_state in config.MENU_STATES and state in config.GAME_STATES:
            new_interface = self._game
        elif old_state == config.GS_LOADING:
            if state in config.GAME_STATES:
                new_interface = self._game
            elif state in config.MENU_STATES:
                new_interface = self._menu
        
        if state in config.GAME_STATES:
            self._game.change_state(state)
        elif state in config.MENU_STATES:
            self._menu.change_state(state)
        
        self._view.change_state(state, new_interface)
    
    def add_score(self, name, score):
        """ Add the given name and score to the high scores list. If the score
        given is too low for the high scores list, nothing is done. Return the
        index at which the score was added, or -1 if it wasn't added.
        
        _add_score(string, int) -> int
        """
        
        index = -1
        for i, highscore in enumerate(self._highscores):
            if score > highscore[1]:
                self._highscores.insert(i, (name, score))
                self._highscores.pop()
                index = i
                break
        self._save_highscores()
        return index
    
    def _is_highscore(self, score):
        """ Return true if the given score is a high score.
        
        _is_highscore(int) -> bool
        Precondition: The high scores file has been previously loaded.
        """
        
        scores = [n[1] for n in self._highscores]
        return score > min(scores)
    
    def _save_highscores(self):
        """ Save the high scores list to file. The high scores filename is set
        in the configuration file and this method assumes the file exists and is
        writeable. """
        
        file_handle = open(config.highscores_filename, 'w')
        for highscore in self._highscores:
            file_handle.write(highscore[0] + ',' + str(highscore[1]) + '\n')
        file_handle.close()
    
    def _load_highscores(self):
        """ Load the high scores list from file. The high scores filename is set
        in the configuration file and this method assumes the file exists and is
        readable. """
        
        self._highscores = []
        file_handle = open(config.highscores_filename, 'r')
        for line in file_handle:
            name, score = line.split(',')
            score = int(score)
            self._highscores.append((name, score))
        file_handle.close()


def main():
    """ Create and run the application. This method is the main entry point
    into the application. """
    
    app = Polyominohs()
    app.run()


if __name__ == '__main__':
    main()
