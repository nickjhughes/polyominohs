
""" event_handler.py: Contains the Event_Handler class. """


from pygame.constants import *

import config


class Event_Handler:
    
    """ A class for handling events, including keyboard input. """
    
    def __init__(self, pygame):
        """ Initialise.
        
        __init__(pygame) -> void
        """
        
        self._pygame = pygame
        self._filter = [KEYDOWN, KEYUP, QUIT]
        self._filter.extend(config.CUSTOM_EVENTS)
    
    def clear_queue(self):
        """ Clear the events queue. """
        
        self._pygame.event.clear(self._filter)
    
    def get_events(self):
        """ Return all events which have occured since the method
        was last called, as a list. Events not useful are filtered out.
        
        get_events() -> list<pygame.event>
        """
        
        return [e for e in self._pygame.event.get() if e.type in self._filter]
