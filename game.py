
""" game.py: Contains the Game class. """


import random
import pygame.constants as constants
import pygame.time
import pygame.event

import config
from field import *
from generator import *
from omino import *


class Game:
    
    """ The game class which handles the application while in the game. """
    
    def __init__(self, master, view, event_handler, sound, level, order, ominoes):
        """ Initialise a new game with the given level and order, and given
        list of ominoes.
        
        __init__(Ominohs, View, Event_Handler, Sound, int, int,
                 (list<list<list<bool>>>, list<(int, int, int)>)) -> void
        """
        
        self._master = master
        self._view = view
        self._events = event_handler
        self._sound = sound
        self._order = order
        self._level = level
        
        self._score = 0
        self._lines = 0
        
        if order < 5:
            width = 10
            height = 20
        else:
            width = 15
            height = 30
        self._field = Field(order, width, height)
        
        self._droptime = config.levels[self._level]
        
        self._ominoes = ominoes[0]
        self._colours = ominoes[1]
        
        self._next = self._choose_omino()
        
        self._state = None
    
    def get_order(self):
        """ Return the polyomino order of the game.
        
        get_order() -> int
        """
        
        return self._order
    
    def get_score(self):
        """ Return the current score.
        
        get_score() -> int
        """
        
        return self._score
    
    def get_lines_cleared(self):
        """ Return the number of lines cleared in the game.
        
        get_lines_cleared() -> int
        """
        
        return self._lines
    
    def get_field(self):
        """ Return the field object associated with the game.
        
        get_field() -> Field
        """
        
        return self._field
    
    def get_next_omino(self):
        """ Return the omino that is coming up next.
        
        get_next_omino() -> Omino
        """
        
        return self._next
    
    def change_state(self, state):
        """ Change the state of the game.
        
        change_state(int) -> void
        """
        
        self._state = state
    
    def loop(self):
        """ Main game loop which handles user input and updates the game.
        Return the game's score. If None is returned, the application should
        end. If -1 is returned, the game was quit prematurely and the
        application should return the menu.
        
        loop() -> int
        """
        
        clock = pygame.time.Clock()
        self._events.clear_queue()
        
        self._field.add_omino(self._next)
        self._next = self._choose_omino()
        
        pygame.time.set_timer(config.EVENT_FALL, self._droptime)        
        accel_points = 0
        
        self._sound.play_next()
        
        loop = True
        while loop == True:
            
            # Events
            for event in self._events.get_events():
                
                # Music stopped
                if event.type == config.EVENT_MUSIC_STOP:
                    self._sound.play_next()
                
                # In game
                if self._state == config.GS_GAME:
                    
                    if event.type == constants.KEYDOWN:
                        if event.key == constants.K_UP:
                            # Rotate
                            if self._field.rotate_omino():
                                self._sound.play_sound_effect(config.SFX_OMINO_ROTATE)
                        elif event.key == constants.K_LEFT:
                            # Move left
                            pygame.time.set_timer(config.EVENT_MOVE_LEFT,
                                                  config.key_repeat_time)
                            if self._field.move_omino(1):
                                self._sound.play_sound_effect(config.SFX_OMINO_MOVE)
                        elif event.key == constants.K_RIGHT:
                            # Move right
                            pygame.time.set_timer(config.EVENT_MOVE_RIGHT,
                                                  config.key_repeat_time)
                            if self._field.move_omino(2):
                                self._sound.play_sound_effect(config.SFX_OMINO_MOVE)
                        elif event.key == constants.K_DOWN:
                            # Move down
                            pygame.time.set_timer(config.EVENT_MOVE_DOWN,
                                                  config.key_repeat_time)
                            if self._field.move_omino():
                                accel_points += 1
                        elif event.key == constants.K_ESCAPE:
                            # Pause
                            self._sound.play_sound_effect(config.SFX_PAUSE)
                            pygame.time.set_timer(config.EVENT_FALL, 0)
                            self._master.change_state(config.GS_GAME_PAUSED)
                        elif event.key == constants.K_SPACE:
                            # Drop
                            while self._field.get_omino():
                                self._field.move_omino()
                            accel_points += 20
                    
                    elif event.type == constants.KEYUP:
                        if event.key == constants.K_LEFT:
                            pygame.time.set_timer(config.EVENT_MOVE_LEFT, 0)
                        elif event.key == constants.K_RIGHT:
                            pygame.time.set_timer(config.EVENT_MOVE_RIGHT, 0)
                        elif event.key == constants.K_DOWN:
                            pygame.time.set_timer(config.EVENT_MOVE_DOWN, 0)
                    
                    elif event.type == config.EVENT_FALL:
                        self._field.move_omino()
                    
                    # Keys held down
                    elif event.type == config.EVENT_MOVE_LEFT:
                        if self._field.move_omino(1):
                            self._sound.play_sound_effect(config.SFX_OMINO_MOVE)
                    elif event.type == config.EVENT_MOVE_RIGHT:
                        if self._field.move_omino(2):
                            self._sound.play_sound_effect(config.SFX_OMINO_MOVE)
                    elif event.type == config.EVENT_MOVE_DOWN:
                        if self._field.move_omino():
                                accel_points += 1
                
                # Game paused
                elif self._state == config.GS_GAME_PAUSED:
                    if event.type == constants.KEYDOWN:
                        if event.key == constants.K_ESCAPE:
                            # Un-pause
                            pygame.time.set_timer(config.EVENT_FALL, 500)
                            self._master.change_state(config.GS_GAME)
                        elif event.key == constants.K_y:
                            # Quit back to menu
                            self._sound.stop_music()
                            return -1
                
                # Game over screen
                elif self._state == config.GS_GAME_OVER:
                    if event.type == constants.KEYDOWN:
                        if event.key == constants.K_RETURN:
                            loop = False
                
                if event.type == constants.QUIT:
                    return None
            
            # Handle the omino being settled and either game over or new omino
            if self._state == config.GS_GAME:
                if not self._field.get_omino():
                    lines_cleared = self._field.check()
                    if lines_cleared > 0:
                        self._sound.play_sound_effect(config.SFX_LINE_CLEAR)
                        self._lines += lines_cleared
                        points = lines_cleared * 50
                        if lines_cleared == self._order:
                            points *= 2
                        points += accel_points
                        self._score += points
                    else:
                        self._sound.play_sound_effect(config.SFX_OMINO_LAND)
                        self._score += accel_points
                    if self._field.add_omino(self._next):
                        self._next = self._choose_omino()
                        pygame.time.set_timer(config.EVENT_FALL, self._droptime)
                        accel_points = 0
                    else:
                        # Game over
                        self._sound.stop_music()
                        self._sound.play_sound_effect(config.SFX_GAME_OVER)
                        pygame.time.set_timer(config.EVENT_FALL, 0)
                        self._master.change_state(config.GS_GAME_OVER)
            
            self._view.update()
            clock.tick(60)
        
        return self._score
    
    def _choose_omino(self):
        """ Choose a random omino from the list of ominoes of the game's order
        and return it.
        
        _choose_omino() -> Omino
        """
        
        x = random.randint(0, len(self._ominoes) - 1)
        omino = Omino(self._ominoes[x], self._colours[x])
        return omino