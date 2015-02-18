
""" field.py: Contains the Field class. """


import random
import copy

from helpers import *


class Field:
    
    """ A class representing the game's playing field which is a grid
    of blocks and a moving omino. The grid is a 2D list of pairs of the form
    (bool, (int, int, int)) representing block on/off and block RGB colour
    respectively.
    """
    
    def __init__(self, order, width, height):
        """ Initalise an empty playing grid of size width * height, for
        playing with polyominoes of the given order.
        
        __init__(int, int, int) -> void
        """
        
        self._width = width
        self._height = height
        self._order = order
        self._grid = rect_list(width, height, (False, (0, 0, 0)))
        self._omino = None
    
    def get_size(self):
        """ Return a pair giving the width and height of the field.
        
        get_size() -> (int, int)
        """
        
        return (self._width, self._height)
    
    def get_complete_grid(self):
        """ Return a copy of the grid with the currently moving omino baked
        into it.
        
        get_complete_grid() -> list<list<(bool, (int, int, int))>>
        """
        
        if self._omino == None:
            return copy.deepcopy(self._grid)
        
        complete_grid = copy.deepcopy(self._grid)
        for i, line in enumerate(self._omino.get_shape()):
            for j in xrange(self._order):
                if self._omino.get_location().y + i < self._height \
                   and self._omino.get_location().x + j < self._width \
                   and line[j]:
                    block = (True, self._omino.get_colour())
                    row = self._omino.get_location().y + i
                    column = self._omino.get_location().x + j
                    complete_grid[row][column] = block
        return complete_grid
    
    def get_omino(self):
        """ Return the omino currently in the field, if there is one. If there
        is not, return None.
        
        get_omino() -> Omino/None
        """
        
        return self._omino
    
    def add_omino(self, omino):
        """ Drop the given omino into the top of the grid. Return False if
        the block cannot be added (in any rotation) because others are in
        the way. If there is already a moving omino the field if will be
        replaced.
        
        add_omino(Omino) -> bool
        """
        
        self._omino = omino
        x = int(self._width / 2 - int(round(self._omino.get_width() / 2.0)))
        y = 0
        shape = self._omino.get_shape()
        
        # Put top of omino at top of grid
        for row in shape:
            if not row.count(True):
                y -= 1
            else:
                break
        
        location = Point(x, y)
        if self._check_collision(location):
            # Check all rotations if given one causes a collision
            rotations = [rotation for rotation in [0, 1, 2, 3] if not \
                         self._check_collision(location, rotation)]
            if not rotations:
                # Can't drop the omino in any rotation
                self._omino = None
                return False
            else:
                random.shuffle(rotations)
                self._omino.move(location)
                self._omino.rotate(rotations[0])
                return True
        else:
            self._omino.move(location)
            return True
    
    def move_omino(self, direction=0):
        """ Try to move the current omino in the given direction and return
        True or False depending on success. If moving the omino settles it in
        the grid, bake it into the grid. For direction: 0=down, 1=left, 2=right
        
        move_omino(int) -> bool
        Precondition: direction, if given, is 0, 1 or 2.
        """
        
        if not self._omino: return False
        current_x = self._omino.get_location().x
        current_y = self._omino.get_location().y
        if direction == 0:
            # Move down
            new_location = Point(current_x, current_y + 1)
            if self._check_collision(new_location):
                # Hit the ground or a stale block, so bake omino into the grid
                self._grid = self.get_complete_grid()
                self._omino = None
                return False
            else:
                self._omino.move(new_location)
                return True
        elif direction == 1:
            # Move left
            new_location = Point(current_x - 1, current_y)
            if not self._check_collision(new_location):
                self._omino.move(new_location)
                return True
            else:
                return False
        elif direction == 2:
            # Move right
            new_location = Point(current_x + 1, current_y)
            if not self._check_collision(new_location):
                self._omino.move(new_location)
                return True
            else:
                return False
    
    def rotate_omino(self):
        """ Rotate the current omino clockwise 90 degrees, if possible. Return
        True if successful, or False if not.
        
        rotate_omino() -> bool
        """
        
        if not self._omino: return
        
        old_rotation = self._omino.get_rotation()
        new_rotation = (old_rotation + 1) % 4
        
        location = self._omino.get_location()
        if self._omino.get_pivot() != Point(-1, -1):
            # Offset by correct amount (see Omino.rotate() comments)
            old_offset = self._omino.get_offset(old_rotation)
            new_offset = self._omino.get_offset(new_rotation)
            offset = old_offset - new_offset
            location += offset
        
        if not self._check_collision(location, new_rotation):
            self._omino.rotate()
            return True
        else:
            return False
    
    def check(self):
        """ Check grid for full lines and clear them. Return number of lines
        cleared.
        
        check() -> int
        """
        
        full_lines = []
        for row in xrange(self._height):
            if [n[0] for n in self._grid[row]].count(True) == self._width:
                full_lines.append(row)
        if full_lines:
            # Clear row and move all rows above down
            for row in full_lines:
                for column in xrange(self._width):
                    self._grid[row][column] = (False, 0)
                for above_row in xrange(row, 0, -1):
                    for column in xrange(self._width):
                        self._grid[above_row][column] = self._grid[above_row - 1][column]
        return len(full_lines)
    
    def _check_collision(self, location, rotation=None):
        """ Return True if the omino location and rotation given will make
        the omino collide with any stale block or the borders of the grid.
        If rotation is not given, the omino's current rotation is used.
        
        _check_collision(Point, int) -> bool
        Precondition: location is a valid point in the grid.
        """
        
        if not self._omino: return
        shape = self._omino.get_shape(rotation)
        for row in xrange(self._order):
            for column in xrange(self._order):
                if shape[row][column]:
                    if location.y + row > self._height - 1 \
                       or location.y + row < 0:
                        # Hit floor or roof
                        return True
                    if location.x + column < 0 \
                       or location.x + column > self._width - 1:
                        # Hit left or right walls
                        return True
                    if self._grid[location.y + row][location.x + column][0]:
                        # Hit a stale block
                        return True
        return False
