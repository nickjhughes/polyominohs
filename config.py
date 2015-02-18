
""" config.py: All variables that have the possibility of being changed in the
future are centralised here for easier adjustment. Also contains constants
definitions. """


import os

# Resources locations
resources_dir = 'resources'
highscores_filename = os.path.join(resources_dir, 'highscores')
font = os.path.join(resources_dir, 'fonts', 'fff_spacedust.ttf')
music_dir = os.path.join(resources_dir, 'music')
sfx_dir = os.path.join(resources_dir, 'sfx')
music_filenames = ['tetrisa.mid', 'tetrisb.mid', 'tetrisc.mid']
sfx_filenames = ['menu_move.wav', 'menu_select.wav', 'omino_move.wav',
                 'omino_rotate.wav', 'omino_land.wav', 'line_clear.wav',
                 'pause.wav', 'game_over.wav']

# How quickly (in ms) omino drops at each difficulty level
levels = {1: 500, 2: 400, 3: 300, 4: 250, 5: 200, 6: 150, 7: 100, 8: 50, 9: 25}

# How often the event happens (in ms) when a key is held down
key_repeat_time = 100

# The size (in pixels) of the omino blocks at each order
sizes = {1: 21, 2: 21, 3: 21, 4: 21, 5: 14, 6: 14}

# Text
names = {1: 'monomino', 2: 'domino', 3: 'tromino',
         4: 'tetromino', 5: 'pentomino', 6: 'hexomino'}
instructions = '''PolyominOhs! is played in an identical way to Tetris, except that the blocks used are of the order you choose. The order is the number of squares which make up each block. For standard Tetris this is 4, and they are tetrominoes.'''


# Constants

# Sound effects
SFX_MENU_MOVE = 0
SFX_MENU_SELECT = 1
SFX_OMINO_MOVE = 2
SFX_OMINO_ROTATE = 3
SFX_OMINO_LAND = 4
SFX_LINE_CLEAR = 5
SFX_PAUSE = 6
SFX_GAME_OVER = 7

# Custom events
EVENT_FALL = 24
EVENT_MUSIC_STOP = 25
EVENT_MOVE_LEFT = 26
EVENT_MOVE_RIGHT = 27
EVENT_MOVE_DOWN = 28
CUSTOM_EVENTS = [EVENT_FALL, EVENT_MUSIC_STOP, EVENT_MOVE_LEFT,
                 EVENT_MOVE_RIGHT, EVENT_MOVE_DOWN]

# Application state
GS_MENU = 0
GS_MENU_HIGHSCORES = 1
GS_MENU_HELP = 2
GS_LOADING = 3
GS_GAME = 4
GS_GAME_PAUSED = 5
GS_GAME_OVER = 6
GS_MENU_ENTER_HIGHSCORE = 7

# Which class (Game or Menu) handles each application state
GAME_STATES = [GS_GAME, GS_GAME_PAUSED, GS_GAME_OVER]
MENU_STATES = [GS_MENU, GS_MENU_HIGHSCORES, GS_MENU_HELP,
               GS_MENU_ENTER_HIGHSCORE]

# Menu selections
MENU_LENGTH = 8  # Number of selections
MENU_START = 0
MENU_HIGHSCORES = 1
MENU_HELP = 2
MENU_QUIT = 3
MENU_LEVEL = 4
MENU_ORDER = 5
MENU_SFX = 6
MENU_MUSIC = 7

# Button states
TXT_NORMAL = 0
TXT_HOVER = 1
TXT_SELECTED = 2