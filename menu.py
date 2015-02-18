
""" menu.py: contains the Menu class. """


import random
import pygame.constants as constants
import pygame.time

import config


class Menu:
    
    """ The menu class which handles the running of the application while
    in the menu. """
    
    def __init__(self, master, view, event_handler, sound, level=1, order=4):
        """ Initialise the menu with the given level and order pre-selected.
        
        __init__(Ominohs, View, Event_Handler, Sound, int, int) -> void
        """
        
        self._master = master
        self._view = view
        self._events = event_handler
        self._sound = sound
        
        self._order = order
        self._level = level
        
        self._sfx = sound.get_sound_effects_on()
        self._music = sound.get_music_on()
        
        self._selected = config.MENU_START
        self._state = None
        
        self._rand_omino = -1
        self._new_random_omino()
        
        self._highscore_name = ['A', '_', '_']
        self._name_selected = 0
        self._alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        self._highlight_score = -1
    
    def change_state(self, state):
        """ Change the state of the menu.
        
        change_state(int) -> void
        """
        
        self._state = state
    
    def get_name_selected(self):
        """ Return the index of the currently selected character in the
        high score name entry window.
        
        get_name_selected() -> int
        """
        
        return self._name_selected
    
    def get_random_omino(self):
        """ Return the number of a random omino of the currently selected order.
        
        get_random_omino() -> int
        """
        
        return self._rand_omino
    
    def get_selection(self):
        """ Return the currently selected menu item.
        
        get_selection() -> int
        """
        
        return self._selected
    
    def get_order(self):
        """ Return the currently selected order.
        
        get_order() -> int
        """
        
        return self._order
    
    def get_level(self):
        """ Return the currently selected difficulty level.
        
        get_level() -> int
        """
        
        return self._level
    
    def get_sfx(self):
        """ Return the currently selected sound effects option.
        
        get_sfx() -> string
        """
        
        return self._sfx
    
    def get_music(self):
        """ Return the currently selected music option.
        
        get_music() -> string
        """
        
        return self._music
    
    def get_highscore_highlight(self):
        """ Return the index of the high score that was just achieved, so that
        it can be highlighted when displayed.
        
        get_highscore_highlight() -> int
        """
        
        return self._highlight_score
    
    def get_highscore_name(self):
        """ Return the name currently being entered for high score.
        
        get_highscore_name() -> list<char>
        """
        
        return self._highscore_name
    
    def loop(self):
        """ Loop while the user uses the menu, then return a pair with the
        options selected for starting a game: (order, level). The application
        should end if (0, 0) is returned.
        
        loop() -> (int, int)
        """
        
        self._events.clear_queue()
        clock = pygame.time.Clock()
        
        # Timer for changing random omino being displayed
        pygame.time.set_timer(constants.USEREVENT, 1000)
        
        while True:
            
            # Events
            for event in self._events.get_events():
                
                # Normal Menu
                if self._state == config.GS_MENU:
                    if event.type == constants.KEYDOWN:
                        if event.key == constants.K_UP:
                            self._selected = (self._selected - 1) % \
                                             config.MENU_LENGTH
                            self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                        elif event.key == constants.K_DOWN:
                            self._selected = (self._selected + 1) % \
                                             config.MENU_LENGTH
                            self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                        elif event.key == constants.K_LEFT:
                            if self._selected == config.MENU_ORDER and \
                               self._order > 1:
                                self._order -= 1
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                                self._new_random_omino()
                            elif self._selected == config.MENU_LEVEL and \
                                 self._level > 1:
                                self._level -= 1
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                            elif self._selected == config.MENU_SFX and \
                                 self._sfx == 'Off':
                                self._sfx = 'On'
                                self._sound.toggle_sound_effects()
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                            elif self._selected == config.MENU_MUSIC and \
                                 self._music == 'Off':
                                self._music = 'On'
                                self._sound.toggle_music()
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                        elif event.key == constants.K_RIGHT:
                            if self._selected == config.MENU_ORDER and \
                               self._order < 6:
                                self._order += 1
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                                self._new_random_omino()
                            elif self._selected == config.MENU_LEVEL and \
                                 self._level < 9:
                                self._level += 1
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                            elif self._selected == config.MENU_SFX and \
                                 self._sfx == 'On':
                                self._sfx = 'Off'
                                self._sound.toggle_sound_effects()
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                            elif self._selected == config.MENU_MUSIC and \
                                 self._music == 'On':
                                self._music = 'Off'
                                self._sound.toggle_music()
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                        elif event.key == constants.K_RETURN:
                            if self._selected == config.MENU_START:
                                self._sound.play_sound_effect(config.SFX_MENU_SELECT)
                                return (self._order, self._level)
                            elif self._selected == config.MENU_QUIT:
                                self._sound.play_sound_effect(config.SFX_MENU_SELECT)
                                return (0, 0)
                            elif self._selected == config.MENU_HELP:
                                self._sound.play_sound_effect(config.SFX_MENU_SELECT)
                                self._master.change_state(config.GS_MENU_HELP)
                            elif self._selected == config.MENU_HIGHSCORES:
                                self._sound.play_sound_effect(config.SFX_MENU_SELECT)
                                self._master.change_state(config.GS_MENU_HIGHSCORES)
                    elif event.type == constants.USEREVENT:
                        self._new_random_omino()
                
                # Help or highscores being shown
                elif self._state in [config.GS_MENU_HELP,
                                     config.GS_MENU_HIGHSCORES]:
                    if event.type == constants.KEYDOWN:
                        if event.key in [constants.K_RETURN, constants.K_ESCAPE]:
                            self._sound.play_sound_effect(config.SFX_MENU_SELECT)
                            self._highlight_score = -1
                            self._master.change_state(config.GS_MENU)
                
                # Enter highscore
                elif self._state == config.GS_MENU_ENTER_HIGHSCORE:
                    if event.type == constants.KEYDOWN:
                        if event.key == constants.K_RETURN:
                            self._sound.play_sound_effect(config.SFX_MENU_SELECT)
                            index = self._master.add_score(''.join(self._highscore_name),
                                                           self.highscore)
                            self._highlight_score = index
                            self._master.change_state(config.GS_MENU_HIGHSCORES)
                        elif event.key == constants.K_LEFT:
                            if self._name_selected > 0:
                                self._name_selected -= 1
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                        elif event.key == constants.K_RIGHT:
                            if self._name_selected < 2:
                                self._name_selected += 1
                                self._sound.play_sound_effect(config.SFX_MENU_MOVE)
                        elif event.key == constants.K_UP:
                            current = self._highscore_name[self._name_selected]
                            self._highscore_name[self._name_selected] = \
                                self._next_letter(current, -1)
                        elif event.key == constants.K_DOWN:
                            current = self._highscore_name[self._name_selected]
                            self._highscore_name[self._name_selected] = \
                                self._next_letter(current)
                
                if event.type == constants.QUIT:
                    return (0, 0)
            
            self._view.update()
            clock.tick(60)
        
        pygame.time.set_timer(constants.USEREVENT, 0)
        return (self._order, self._level)
    
    def _new_random_omino(self):
        """ Generate a new random omino number of the currently selected order.
        """
        
        if self._order in [1, 2]:
            new = 0
        else:
            max = len(self._master._ominoes[self._order - 1][0]) - 1
            new = random.randint(0, max)
            while new == self._rand_omino:
                new = random.randint(0, max)
        self._rand_omino = new
    
    def _next_letter(self, letter, direction=1):
        """ Return the next letter of the alphabet, with wrapping. If direction
        is -1, return previous letter.
        
        _next_letter(char, int) -> char
        Precondition: letter is a single uppercase letter of the alphabet.
        """
        
        if not direction in [-1, 1]: direction = 1
        length = len(self._alphabet)
        return self._alphabet[(self._alphabet.find(letter) + direction) % length]
