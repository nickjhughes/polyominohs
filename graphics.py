
""" graphics.py: Contains a number of classes and functions for the graphics
component of the application. Essentially just a lot of helpers for the View
class. """


import math

import config


def hsv2rgb(hsv):
    """ Convert the given HSV triple to an RGB triple.
    (0..359, 0..1, 0..1) -> (0..255, 0..255, 0..255)
    
    hsv2rgb((int, float, float)) -> (int, int, int)
    """
    
    h, s, v = hsv
    hi = int(math.floor(h / 60.0) % 6)
    f = (h / 60.0) - math.floor(h / 60.0)
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = [(v, t, p), (q, v, p), (p, v, t), 
               (p, q, v), (t, p, v), (v, p, q)][hi]
    rgb = (int(r * 255), int(g * 255), int(b * 255))
    return rgb

def rgb2hsv(rgb):
    """ Convert the given RGB triple to a HSV triple.
    (0..255, 0..255, 0..255) -> (0..359, 0..1, 0..1)
    
    rgb2hsv((int, int, int)) -> (int, float, float)
    """
    
    correct_rgb = (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    r, g, b = correct_rgb
    maximum = max(correct_rgb)
    minimum = min(correct_rgb)
    
    if maximum == minimum:
        h = 0
    elif maximum == r:
        h = (60 * ((g - b) / (maximum - minimum))) % 360
    elif maximum == g:
        h = 60 * ((b - r) / (maximum - minimum)) + 120
    elif maximum == b:
        h = 60 * ((r - g) / (maximum - minimum)) + 240
    h = round(h)
    if maximum == 0:
        s = 0
    else:
        s = 1 - minimum / maximum 
    v = maximum
    
    return (h, s, v)

def draw_grid(surface, coords, grid, size, pygame):
    """ Draw the grid of blocks to the given surface at (left, top) coordinates,
    with blocks of given size.
    
    draw_grid(pygame.Surface, (int, int),
              list<list<(bool, (int, int, int))>>, int, pygame) -> void
    """
    
    left, top = coords
    height = len(grid)
    width = len(grid[0])
    
    for row in xrange(height):
        for col in xrange(width):
            if grid[row][col][0]:
                colour = grid[row][col][1]
                block_left = left + col * (size - 1)
                block_top = top + row * (size - 1)
                draw_block(surface, (block_left, block_top), size, colour, pygame)

def draw_block(surface, coords, size, colour, pygame):
    """ Draw a block of the given colour and size onto the given surface at
    (left, top) coordinates.
    
    draw_block(pygame.Surface, (int, int), int, (int, int, int), pygame) -> void
    """
    
    left, top = coords
    h, s, v = rgb2hsv(colour)
    highlight_colour = hsv2rgb((h, s, 1.0))
    shadow_colour = hsv2rgb((h, s, 0.57))
    
    # Outline
    rect = pygame.Rect(left, top, size, size)
    pygame.draw.rect(surface, (255, 255, 255), rect, 1)
    # Cut out corners
    surface.set_at((left, top), (0, 0, 0))
    surface.set_at((left + size - 1, top), (0, 0, 0))
    surface.set_at((left, top + size - 1), (0, 0, 0))
    surface.set_at((left + size - 1, top + size - 1), (0, 0, 0))
    # Fill
    rect = pygame.Rect(left + 1, top + 1, size - 2, size - 2)
    pygame.draw.rect(surface, colour, rect, 0)
    # Highlight
    rect = pygame.Rect(left + 1, top + 1, size - 2, 2)
    pygame.draw.rect(surface, highlight_colour, rect, 0)
    rect = pygame.Rect(left + 1, top + 1, 2, size - 4)
    pygame.draw.rect(surface, highlight_colour, rect, 0)
    # Shadow
    rect = pygame.Rect(left + 1, top + size - 3, size - 2, 2)
    pygame.draw.rect(surface, shadow_colour, rect, 0)
    rect = pygame.Rect(left + size - 3, top + 3, 2, size - 4)
    pygame.draw.rect(surface, shadow_colour, rect, 0)

def draw_polyomino(surface, coords, shape, size, colour, pygame):
    """ Draw the given polyomino in the given colour and size to the given
    surface at (left, top) coordinates.
    
    draw_polyomino(pygame.Surface, (int, int), list<list<bool>>, int,
                   (int, int, int), pygame) -> void
    """
    
    left, top = coords
    order = len(shape)
    
    block = pygame.Surface((size, size))
    block = block.convert()
    block.fill((0, 0, 0))
    block.set_colorkey((0, 0, 0))
    draw_block(block, (0, 0), size, colour, pygame)
    
    # Adjust for empty rows at top
    for row in shape:
        if row.count(True) == 0:
            top -= size
        else:
            break
    
    for row in xrange(order):
        for col in xrange(order):
            if shape[row][col]:
                block_top = top + row * (size - 1)
                block_left = left + col * (size - 1)
                surface.blit(block, (block_left, block_top))

def draw_border(surface, colour, pygame):
    """ Draw a two pixel border of colour and a two pixel border of white
    separated by one pixel, around the given surface.
    
    draw_border(pygame.Surface, (int, int, int), pygame) -> void
    """
    
    w, h = surface.get_width(), surface.get_height()
    outer_rect = pygame.Rect(0, 0, w - 1, h - 1)
    pygame.draw.rect(surface, colour, outer_rect, 2)
    inner_rect = pygame.Rect(3, 3, w - 7, h - 7)
    pygame.draw.rect(surface, (255, 255, 255), inner_rect, 2)

def draw_text(surface, coords, text, size, colour, pygame, outline=False):
    """ Draw the given text of given size and colour, at (left, top)
    coordinates, to the given surface. If outline is True, the text will be
    drawn white with a one pixel outline of the given colour.
    
    draw_text(pygame.Surface, (int, int), string, int, (int, int, int),
              pygame, bool) -> void
    """
    
    left, top = coords
    if not outline:
        font = pygame.font.Font(config.font, size)
        render = font.render(text, False, colour)
        pos = render.get_rect()
        pos.left = left
        pos.top = top
        surface.blit(render, pos)
    else:
        font = pygame.font.Font(config.font, size)
        surface.blit(hollow_text(font, text, colour, pygame), (left, top))
        render = font.render(text, False, (255, 255, 255))
        pos = render.get_rect()
        pos.left = left + 1
        pos.top = top + 1
        surface.blit(render, pos)

class Text_Entry:
    
    """ A class for the visual aspect of a text entry field. """
    
    def __init__(self, length, default, size, coords):
        """ Initialise with the given attributes. Coordinates are (left, top).
        
        __init__(int, list<char>, int, (int, int)) -> void
        Precondition: default has a size of length.
        """
        
        self._length = length
        self._text = default
        self._size = size
        self._left, self._top = coords
        
        # For bouncy text
        self._ypos = 0
        self._yvel = 0
        self._yacc = 0.1
    
    def update(self, text):
        """ Update text.
        
        update(list<char>) -> void
        """
        
        self._text = text
    
    def draw(self, surface, selected, colour, pygame):
        """ Draw the text field to the given surface.
        
        draw(pygame.Surface, int, (int, int, int), pygame) -> void
        Precondition: selected is less than the length of the field.
        """
        
        left = self._left
        for i, char in enumerate(self._text):
            if selected == i:
                # For bouncy text
                self._yvel += self._yacc
                self._ypos += self._yvel
                if self._ypos > 5:
                    self._ypos = 5
                    self._yvel = -self._yvel
                top = self._top - 2 + self._ypos
                
                draw_text(surface, (left, top), char, self._size, colour,
                          pygame, True)
            else:
                draw_text(surface, (left, self._top), char, self._size,
                          (255, 255, 255), pygame)
            left += self._size + 10

class Radio_Selection:
    
    """ A class for the visual aspect of aradio selection of numerous
    text items. """
    
    def __init__(self, items, size, coords):
        """ Initialise with the given attributes. Coordinates are (left, top).
        
        __init__(list<string>, int, (int, int) -> void
        """
        
        self._size = size
        self._items = items
        self._left, self._top = coords
        
        # For bouncy text
        self._ypos = 0
        self._yvel = 0
        self._yacc = 0.1
    
    def draw(self, surface, selected, mode, colour, pygame):
        """ Draw the radio selection widget to the given surface. Mode should
        be one of (TXT_HOVER, TXT_NORMAL).
        
        draw(pygame.Surface, int, int, (int, int, int), pygame) -> void
        """
        
        left = self._left
        for i, item in enumerate(self._items):
            if mode == config.TXT_HOVER and selected == item:
                # For bouncy text
                self._yvel += self._yacc
                self._ypos += self._yvel
                if self._ypos > 5:
                    self._ypos = 5
                    self._yvel = -self._yvel
                top = self._top - 2 + self._ypos
                
                draw_text(surface, (left, top), item, self._size,
                          colour, pygame, True)
            elif mode != config.TXT_HOVER and selected == item:
                draw_text(surface, (left, self._top), item, self._size,
                          colour, pygame)
            else:
                draw_text(surface, (left, self._top), item, self._size,
                          (255, 255, 255), pygame)
            left += len(item) * (self._size + 2)

class Button:
    
    """ A class for visual aspect of a button. """
    
    def __init__(self, text, size, coords):
        """ Create a new button with the given text and size and at the
        given coordinates (left, top).
        
        __init__(string, int, (int, int)) -> void
        """
        
        self._size = size
        self._text = text
        self._left, self._top = coords
        
        # For bouncy text
        self._ypos = 0
        self._yvel = 0
        self._yacc = 0.1
    
    def draw(self, surface, mode, pygame, colour=None):
        """ Draw the button to the given surface and of the mode (TXT_NORMAL,
        TXT_HOVER, TXT_SELECTED) given. Colour need only be given when mode
        is TXT_SELECTED or TXT_HOVER.
        
        draw(pygame.Surface, int, pygame, (int, int, int)) -> void
        """
        
        if mode == config.TXT_SELECTED:
            draw_text(surface, (self._left, self._top), self._text, self._size,
                      colour, pygame)
        elif mode == config.TXT_HOVER:
            # For bouncy text
            self._yvel += self._yacc
            self._ypos += self._yvel
            if self._ypos > 5:
                self._ypos = 5
                self._yvel = -self._yvel
            top = self._top - 2 + self._ypos
            
            draw_text(surface, (self._left, top), self._text, self._size,
                      colour, pygame, True)
        else:
            draw_text(surface, (self._left, self._top), self._text, self._size,
                      (255, 255, 255), pygame)



# The following method was originally written by Pete Shinners
# (Pete@shinners.org) and was obtained from the pygame Code Repository 
# (http://www.pygame.org/pcr/).
def hollow_text(font, message, fontcolor, pygame):
    """ Return a surface with the given message rendered as an outline.
    
    hollow_text(pygame.Font, string, (int, int, int), pygame) -> pygame.Surface
    """
    
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img


# The following code (exception class and textrect method) was originally
# written by David Clark (da_clark@shaw.ca) and was obtained from the pygame
# Code Repository (http://www.pygame.org/pcr/).

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, size, rect, text_color, background_color,
                    justification, pygame):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """
    
    font = pygame.font.Font(config.font, size)
    
    final_lines = []
    
    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface
