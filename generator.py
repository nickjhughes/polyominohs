
""" generator.py: Contains the Generator class. """


import random
import copy

import graphics
from helpers import *


# Just to check we have generated the correct number of polyominoes
# {order: number of omiones}
counts = {1: 1, 2: 1, 3: 2, 4: 7, 5: 18, 6: 60}


class Generator:
    
    """ A class for generating polyominoes. Call the generate function with the
    polyomino order wanted. Please Note: This class has not been tested for
    orders greater than 6. """
    
    def generate(self, order):
        """ Return a list of all the one-sided polyominoes of the given order.
        Objects in returned list are 2D square lists representing the shape of
        the polyominoes by boolean values.
        
        generate(int) -> list<list<list<bool>>>
        """
        
        self._order = order
        ominoes = []
        
        if order == 1:
            ominoes = [[[True]]]
            return ominoes
        
        # This is the 'growth method' algorithm for generating polyominoes.
        # A order * order grid is made, then the bottom-left block filled.
        # The squares adjacent to that block are numbered, and one of them
        # is randomly picked. This continues till order blocks are filled.
        # Check to see if generated polyomino is a repeat, and continue
        # till we've generated enough.
        
        while len(ominoes) < counts[order]:
            free_squares = {}
            pick = 0
            max_number = 0
            omino = rect_list(order, order, False)
            if order > 4:
                # A different starting point for orders > 4
                # This is so crosses and similar shapes can be generated
                row, col = order - 2, 0
            else:
                row, col = order - 1, 0
            omino[row][col] = True
            for s in xrange(order - 1):
                free_squares, max_number = self._number_adjacent_squares(omino,
                                           (row, col), free_squares, max_number)
                possible = [n for n in free_squares.keys() if n > pick]
                pick = random.choice(possible)
                row, col = free_squares[pick]
                free_squares.pop(pick)
                omino[row][col] = True
            omino = self._normalise(omino)
            if not [n for n in ominoes if n == omino]:
                ominoes.append(omino)
        
        return ominoes
    
    def generate_colours(self, n):
        """ Generate n unique colours and return as a list of RGB triples.
        Colours are as contrasted as possible.
        
        generate_colours(int) -> list<(int, int, int)>
        """
        
        # This divides the 360 degrees of hue in the HSV colour space by n,
        # and so chooses n colours with equally spaced hues.
        
        colours = []
        degrees = 360 / n
        for i in xrange(n):
            hsv = (degrees * i, 1.0, 0.78)
            rgb = graphics.hsv2rgb(hsv)
            colours.append(rgb)
        return colours
    
    def _normalise(self, polyomino):
        """ Return a copy of the given polyomino with its rotation and position
        normalised. That is, in its left- and bottom-most position and rotation.
        
        _normalise(list<list<bool>>) -> list<list<bool>>
        """
        
        # Bottom- and left-most rotation and position is defined here as the
        # position in which the most bottom row and left column squares are
        # filled.
        
        adjusted = copy.deepcopy(polyomino)
        rowfractions = {}   # Fraction of bottom row filled
        colfractions = {}   # Fraction of left column filled
        for rotation in xrange(4):
            adjusted = self._move(adjusted)
            rowfilled = adjusted[self._order - 1].count(True)
            rowfraction = float(rowfilled) / self._order
            rowfractions.update({rotation: rowfraction})
            colfilled = [adjusted[row][0] for row in xrange(self._order)].count(True)
            colfraction = float(colfilled) / self._order
            colfractions.update({rotation: colfraction})
            adjusted = self._rotate(adjusted)
        
        # Pick the rotation with the largest fractions
        rowpick = max(rowfractions.values())
        rowpicked_rotations = [k for k, v in rowfractions.iteritems() \
                               if v == rowpick]
        if len(rowpicked_rotations) > 1:
            colpick = max([v for k, v in colfractions.iteritems() \
                           if k in rowpicked_rotations])
            colpicked_rotations = [k for k, v in colfractions.iteritems() \
                                   if v == colpick and k in rowpicked_rotations]
            if len(colpicked_rotations) == 0:
                rotations = rowpicked_rotations[0]
            else:
                rotations = colpicked_rotations[0]
        else:
            rotations = rowpicked_rotations[0]
        
        normalised = copy.deepcopy(polyomino)
        for rotation in xrange(rotations):
            normalised = self._rotate(normalised)
        normalised = self._move(normalised)
        return normalised
    
    def _move(self, polyomino):
        """ Return a copy of the given polyomino pushed into the bottom left
        corner of its grid.
        
        _move(list<list<bool>>) -> list<list<bool>>
        """
        
        moved = copy.deepcopy(polyomino)
        while moved[self._order - 1].count(True) == 0:
            # While bottom row is empty, move down
            for row in xrange(self._order - 1, 0, -1):
                for col in xrange(self._order):
                    moved[row][col] = moved[row - 1][col]
            moved[0] = [False] * self._order
        while [moved[row][0] for row in xrange(self._order)].count(True) == 0:
            # While left column is empty, move left
            for row in xrange(self._order):
                for col in xrange(self._order - 1):
                    moved[row][col] = moved[row][col + 1]
            for row in xrange(self._order):
                moved[row][self._order - 1] = False
        return moved
    
    def _rotate(self, polyomino):
        """ Return a copy of the given polyomino rotated clockwise 90 degrees.
        
        _rotate(list<list<bool>>) -> list<list<bool>>
        """
        
        rotated = rect_list(self._order, self._order, False)
        for row in xrange(self._order):
            for col in xrange(self._order):
                rotated[col][self._order - 1 - row] = polyomino[row][col]
        return rotated
    
    def _number_adjacent_squares(self, polyomino, coordinates, \
                                 numbered_squares, max_number):
        """ Return a pair with a dictionary of all the adjacent squares in the
        given polyomino, keyed by their number, where they are numbered
        clockwise from the top, and the highest numbered square. Numbering will
        start from max_number and any previously numbered squares in
        numbered_squares will be included.
        
        _number_adjacent_squares(list<list<bool>>, (int,int), 
                                 dict<int:(int,int)>, int) ->
                                 (dict<int:(int, int)>, int)
        """
        
        row, col = coordinates
        possible_squares = [(row - 1, col), (row, col + 1),
                            (row + 1, col), (row, col - 1)]
        adjacents = copy.deepcopy(numbered_squares)
        n = max_number
        for row, col in possible_squares:
            if row in range(self._order) and col in range(self._order) \
            and not polyomino[row][col] \
            and not (row, col) in numbered_squares.values():
                # Number the square only if its in the grid, not already
                # numbered and not already filled
                n += 1
                adjacents.update({n: (row, col)})
        return adjacents, n
    