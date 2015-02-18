
""" sound.py: Contains the Sound class. """


import os

import config


class Sound:
    
    """ A class for the audio component of the game. Audio file locations
    are defined in the config file. """
    
    def __init__(self, pygame):
        """ Initialise and load audio.
        
        __init__(pygame) -> void
        """
        
        self._mixer = pygame.mixer
        self._mixer.init()
        self._available = self._mixer.get_init()
        if self._available:
            self._load_audio()
            self._sfx_chan = self._mixer.Channel(0)
        self._music_on = True
        self._sfx_on = True
        self._current_track = -1
    
    def get_music_on(self):
        """ Return 'On' or 'Off' if the music is on or off.
        
        get_music_on() -> string
        """
        
        if self._music_on:
            return 'On'
        else:
            return 'Off'
    
    def get_sound_effects_on(self):
        """ Return 'On' or 'Off' if the sound effects are on or off.
        
        get_sound_effects_on() -> string
        """
        
        if self._sfx_on:
            return 'On'
        else:
            return 'Off'
    
    def toggle_music(self):
        """ Toggle whether music plays or not. """
        
        self._music_on = not self._music_on
    
    def toggle_sound_effects(self):
        """ Toggle whether sound effects play or not. """
        
        self._sfx_on = not self._sfx_on
    
    def play_next(self):
        """ Play the next music track and set a custom event to be generated
        when the track stops. """
        
        if not self._available: return
        if not self._music_on: return
        if len(self._music) == 0: return
        
        self._current_track += 1
        self._current_track %= len(self._music)
        self._mixer.music.load(self._music[self._current_track])
        self._mixer.music.play()
        self._mixer.music.set_endevent(config.EVENT_MUSIC_STOP)
    
    def stop_music(self, fadeout_time=0):
        """ Stop the music track currently playing with a fade-out of
        fadeout_time milliseconds. If time isn't given, music is stopped
        without a fade.
        
        stop_music(int) -> void
        """
        
        if not self._available: return
        self._mixer.music.fadeout(fadeout_time)
    
    def play_sound_effect(self, effect):
        """ Play the given sound effect.
        
        play_sound_effect(int) -> void
        Precondition: effect is the number of a sound effect as defined in the
        config file.
        """
        
        if not self._available: return
        if not self._sfx_on: return
        if self._sfx[effect] == None: return
        self._sfx[effect].play()
    
    def _load_audio(self):
        """ Load the sound effects and make sure music files are available for
        streaming. """
        
        self._music = []
        self._sfx = []
        for filename in config.music_filenames:
            path = os.path.join(config.music_dir, filename)
            if os.path.exists(path):
                self._music.append(path)
        for filename in config.sfx_filenames:
            if os.path.exists(os.path.join(config.sfx_dir, filename)):
                path = os.path.join(config.sfx_dir, filename)
                self._sfx.append(self._mixer.Sound(path))
            else:
                self._sfx.append(None)