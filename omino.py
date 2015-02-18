
""" omino.py: Contains the Omino class. """


import random
import copy
import math

from helpers import *


class Omino:
    
    """ A class representing a single polyomino. """
    
    def __init__(self, shape, colour, rotation=None):
        """ Create a new omino. Shape is a square 2D list filled with boolean
        values representing the shape of the omino. Colour is a triple of RGB
        values. Rotation is the rotation state, if left blank a random rotation
        will be chosen.
        
        __init__(list<list<bool>>, (int, int int), int) -> void
        Precondition: If rotation is given it is between 0 and 3 inclusive.
        """
        
        self._shapes = [shape]
        self._order = len(shape)
        self._find_rotations()
        if rotation == None:
            self._rotation = random.randint(0, 3)
        else:
            self._rotation = rotation
        self._colour = colour
        self._location = None
    
    def get_width(self):
        """ Return the actual width of the omino in its current rotation.
        
        get_width() -> int
        """
        
        # Calculates the number of columns with at least one space filled
        cols = []
        for col in xrange(self._order):
            column = []
            for row in xrange(self._order):
                column.append(self.get_shape()[row][col])
            cols.append(column)
        return len([column for column in cols if column.count(True) > 0])
    
    def get_location(self):
        """ Return the current location of the omino.
        
        get_location() -> Point
        """
        
        return self._location
    
    def get_shape(self, rotation=None):
        """ Return the shape of the omino in either the rotation given
        or the omino's current rotation if no rotation is given.
        
        get_shape(int) -> list<list<bool>>
        Precondition: If given rotation it is between 0 and 3 inclusive.
        """
        
        if rotation == None:
            rotation = self._rotation
        return self._shapes[rotation]
    
    def get_rotation(self):
        """ Return an integer representing the omino's current rotation state.
        
        get_rotation() -> int
        """
        
        return self._rotation
    
    def get_colour(self):
        """ Return a triple with the RGB values giving the colour of the omino.
        
        get_colour() -> (int, int, int)
        """
        
        return self._colour
    
    def get_pivot(self):
        """ Return the pivot point of the omino in the form of a Point object.
        
        get_pivot() -> Point
        """
        
        return self._pivot
    
    def get_offset(self, rotation):
        """ Return offset for given rotation.
        
        get_offset(int) -> Point
        Precondition: rotation is between 0 and 3 inclusive
        """
        
        return self._offsets[rotation]
    
    def move(self, location):
        """ Move the omino to the given new location.
        
        move(Point) -> void
        """
        
        self._location = location
    
    def rotate(self, rotation=None):
        """ Rotate the omino to the given state, or if not given rotate by
        90 degrees in the clockwise direction.
        
        rotate(int) -> void
        Precondition: rotation, if given, is between 0 and 3 inclusive.
        """
        
        # The ominos are correctly rotated by just rotating the grid they're in
        # and then moving the omino by the correct amount so that the pivot
        # point stays in the same place. All the 'offset' stuff is related to
        # that.
        
        old_rotation = self._rotation
        if rotation == None:
            self._rotation = (self._rotation + 1) % 4
        else:
            self._rotation = rotation
        if self._pivot != Point(-1, -1):
            # Offset location by correct amount
            offset = self._offsets[old_rotation] - self._offsets[self._rotation]
            self.move(self._location + offset)
	
    def _find_rotations(self):
        """ Find all rotation shapes and offsets of the omino by rotating
        around the pivot point. """
        
        self._find_pivot()
        if self._pivot == Point(-1, -1):
            for i in [1, 2, 3]:
                self._shapes.append(self._shapes[0])
            return
        pivots = [self._pivot]
        self._offsets = [Point(0, 0)]
        for i in [1, 2, 3]:
            shape, rows, cols = self._move(self._rotate_shape(self._shapes[i - 1]))
            self._shapes.append(shape)
            # Find the offsets to rotate correctly and store them
            pivot_x = self._order - 1 - pivots[i - 1].y + cols
            pivot_y = pivots[i - 1].x + rows
            pivots.append(Point(pivot_x, pivot_y))
            self._offsets.append(pivots[-1] - self._pivot)
	
    def _rotate_shape(self, shape):
        """ Return a copy of the given polyomino shape, rotated by 90 degrees
        in the clockwise direction.
        
        _rotate_shape(list<list<bool>>) -> list<list<bool>>
        """
        
        rotated = rect_list(self._order, self._order)
        for row in xrange(self._order):
            for col in xrange(self._order):
                rotated[col][self._order - 1 - row] = shape[row][col]
        return rotated
    
    def _move(self, polyomino):
        """ Return a copy of the given polyomino pushed into the bottom left
        corner of its grid, and the number of rows and columns moved, as a
        triple.
        
        _move(list<list<bool>>) -> (list<list<bool>>, int, int)
        """
        
        moved = copy.deepcopy(polyomino)
        x, y = 0, 0
        while moved[self._order - 1].count(True) == 0:
            # While bottom row is empty, move down
            y += 1
            for row in xrange(self._order - 1, 0, -1):
                for col in xrange(self._order):
                    moved[row][col] = moved[row - 1][col]
            moved[0] = [False] * self._order
        while [moved[row][0] for row in xrange(self._order)].count(True) == 0:
            # While left column is empty, move left
            x += 1
            for row in xrange(self._order):
                for col in xrange(self._order - 1):
                    moved[row][col] = moved[row][col + 1]
            for row in xrange(self._order):
                moved[row][self._order - 1] = False
        return moved, y, x
    
    def _find_pivot(self):
        """ Find the rotational pivot point of the omino and assign it to
        an attribute. """
        
        if self._order == 1:
            self._pivot = Point(0, 0)
            return
        shape = self._shapes[0]
        if self._move(self._rotate_shape(shape))[0] == shape:
            # If the omino is the same after being rotated (eg. a square)
            # a pivot point of (-1, -1) is returned, which indicates it doesn't
            # really need rotating.
            self._pivot = Point(-1, -1)
            return
        cols = []
        for col in xrange(self._order):
            column = []
            for row in xrange(self._order):
                column.append(shape[row][col])
            cols.append(column)
        width = len([column for column in cols if column.count(True) > 0])
        height = len([row for row in shape if row.count(True) > 0])
        # The pivot point is the block closest to the centre of the omino
        # If the centre falls on a line or corner, preference is given to
        # filled blocks (as opposed to empty ones).
        centre = Point(width / 2.0, height / 2.0)
        if centre.x - int(centre.x) == 0.5:
            pivot_x = int(math.ceil(centre.x))
        else:
            x_1 = int(centre.x - 1)
            x_2 = int(centre.x + 1 - 1)
            y = int(self._order - centre.y)
            if not shape[x_1][y] and shape[x_2][y]:
                pivot_x = int(centre.x + 1)
            else:
                pivot_x = int(centre.x)
        if centre.y - int(centre.y) == 0.5:
            pivot_y = int(math.ceil(centre.y))
        else:
            y_1 = int(self._order - centre.y)
            y_2 = int(self._order - centre.y - 1)
            x = pivot_x - 1
            if not shape[x][y_1] and shape[x][y_2]:
                pivot_y = int(centre.y + 1)
            else:
                pivot_y = int(centre.y)
        self._pivot = Point(pivot_x - 1, self._order - pivot_y)
