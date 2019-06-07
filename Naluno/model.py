
from __future__ import division, print_function, unicode_literals

from config import *

__all__ = ['Map', 'Vertex', 'Edge', 'State']


class State:
    FREE = 0
    CLOSED = 1
    MANDATORY = 2
    OPTIONAL = 3


class Square:
    def __init__(self):
        self._has_card = False

    @property
    def has_card(self):
        return self._has_card

    @has_card.setter
    def has_card(self, value):
        self._has_card = value

    def copy_to(self, square):
        square.has_card = self._has_card


class Edge:
    def __init__(self):
        self._port = [State.FREE, State.FREE, State.FREE]
        self._num_cards = 0
        self._contact_number = 0

    @property
    def num_cards(self):
        return self._num_cards

    @num_cards.setter
    def num_cards(self, value):
        self._num_cards = value

    @property
    def port(self):
        return self._port

    @property
    def contact_number(self):
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value):
        self._contact_number = value

    def update(self, edge):
        self._contact_number = 0
        for i in range(3):
            if self.port[i] != State.FREE:
                if self.port[i] != State.CLOSED and edge.port[i] != State.CLOSED:
                    self._contact_number += 1
            self.port[i] = edge.port[i]
        self.num_cards += 1

    def match(self, edge):
        self._contact_number = 0
        if self.port[1] == State.FREE:
            return True
        for i in range(3):
            if self.port[i] == State.MANDATORY:
                if edge.port[i] == State.CLOSED:
                    return False
            elif self.port[i] == State.CLOSED:
                if edge.port[i] == State.MANDATORY:
                    return False
            if self.port[i] != State.CLOSED and edge.port[i] != State.CLOSED:
                self._contact_number += 1
        return True

    @property
    def dock_count(self):
        dock_count = 0
        for i in range(3):
            if self.port[i] == State.MANDATORY or self.port[i] == State.OPTIONAL:
                dock_count += 1
        return dock_count

    @property
    def mandatory_dock_count(self):
        dock_count = 0
        for i in range(3):
            if self.port[i] == State.MANDATORY:
                dock_count += 1
        return dock_count

    def copy_to(self, edge):
        edge.num_cards = self._num_cards
        edge.contact_number = self._contact_number
        for i in range(3):
            edge.port[i] = self._port[i]


class Vertex:
    def __init__(self):
        self._state = State.FREE
        self._contact_number = 0
        self._num_cards = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def contact_number(self):
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value):
        self._contact_number = value

    @property
    def num_cards(self):
        return self._num_cards

    @num_cards.setter
    def num_cards(self, value):
        self._num_cards = value

    def update(self, vertex):
        self._contact_number = 0
        if self._state == State.CLOSED:
            self._state = vertex.state
        elif self._state == State.MANDATORY:
            if vertex.state != State.CLOSED:
                self._state = State.OPTIONAL
                self._contact_number = 1
        elif self._state == State.OPTIONAL:
            if vertex.state != State.CLOSED:
                self._contact_number = 1
        elif self._state == State.FREE:
            self._state = vertex.state
        self._num_cards += 1

    def match(self, vertex):
        self._contact_number = 0
        if self._state == State.FREE:
            return True
        if self._state == State.MANDATORY:
            if vertex.state == State.CLOSED and self._num_cards == 3:
                return False
        elif self._state == State.CLOSED:
            if vertex.state == State.MANDATORY and self._num_cards == 3:
                return False
        if self._state != State.CLOSED and vertex.state != State.CLOSED:
            self._contact_number = 1
        return True

    def copy_to(self, vertex):
        vertex.state = self._state
        vertex.num_cards = self._num_cards
        vertex.contact_number = self._contact_number

    @property
    def dock_count(self):
        if self._state == State.MANDATORY or self._state == State.OPTIONAL:
            return 1
        else:
            return 0

    @property
    def mandatory_dock_count(self):
        if self._state == State.MANDATORY:
            return 1
        else:
            return 0


class Move:
    def __init__(self, card, row, col):
        self._card = card
        self._row = row
        self._col = col

    def get_clone(self):
        return Move(self._card, self._row, self._col)

    @property
    def card(self):
        return self._card

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col


class Map:
    def __init__(self, matrix=None):
        self._most_right_move = None
        self._most_left_move = None
        self._top_move = None
        self._bottom_move = None
        self._contact_count = 0
        self._move_history = []
        self.vsize = VER_MAP_SIZE * 3
        self.hsize = HOR_MAP_SIZE * 3
        self._matrix = []
        self.init_matrix(matrix)

    @property
    def most_right_move(self):
        return self._most_right_move

    @most_right_move.setter
    def most_right_move(self, move):
        self._most_right_move = move

    @property
    def most_left_move(self):
        return self.most_left_move

    @most_left_move.setter
    def most_left_move(self, move):
        self._most_left_move = move

    @property
    def top_move(self):
        return self._top_move

    @top_move.setter
    def top_move(self, move):
        self._top_move = move

    @property
    def bottom_move(self):
        return self._bottom_move

    @bottom_move.setter
    def bottom_move(self, move):
        self._bottom_move = move

    @property
    def contact_count(self):
        return self._contact_count

    @contact_count.setter
    def contact_count(self, value):
        self._contact_count = value

    @property
    def move_history(self):
        return self._move_history

    def init_matrix(self, matrix):
        if matrix is None:
            for i in range(self.vsize):
                row = []
                for j in range(self.hsize):
                    row.append(None)
                self._matrix.append(row)
            tile_row = False
            tile_col = False
            for i in range(self.vsize):
                for j in range(self.hsize):
                    if tile_row:
                        if tile_col:
                            self._matrix[i][j] = Square()
                        else:
                            self._matrix[i][j] = Edge()
                    else:
                        if tile_col:
                            self._matrix[i][j] = Edge()
                        else:
                            self._matrix[i][j] = Vertex()
                    tile_col = not tile_col
                tile_row = not tile_row
                tile_col = False
        else:
            for i in range(self.vsize):
                self._matrix[i].extend(matrix[i, :])

    def clone(self):
        m = Map(self._matrix)
        m.contact_count = self._contact_count
        m.move_history.extend(self._move_history[:])
        m.most_left_move = self._most_left_move
        m.most_right_move = self._most_right_move
        m.top_move = self._top_move
        m.bottom_move = self._bottom_move
        return m

    @property
    def center_col(self):
        return HOR_MAP_SIZE // 2

    @property
    def center_row(self):
        return VER_MAP_SIZE // 2

    def square_at(self, col, row):
        return self._matrix[row * 2 + 1][col * 2 + 1]

    def top_square(self, col, row):
        return self.square_at(col, row - 1)         # NO using GL coord system

    def bottom_square(self, col, row):
        return self.square_at(col, row + 1)         # NO using GL coord system

    def left_square(self, col, row):
        return self.square_at(col - 1, row)

    def right_square(self, col, row):
        return self.square_at(col + 1, row)

    def top_edge(self, col, row):
        return self._matrix[row * 2][col * 2 + 1]

    def bottom_edge(self, col, row):
        return self._matrix[row * 2 + 2][col * 2 + 1]

    def left_edge(self, col, row):
        return self._matrix[row * 2 + 1][col * 2]

    def right_edge(self, col, row):
        return self._matrix[row * 2 + 1][col * 2 + 2]

    def top_left_vertex(self, col, row):
        return self._matrix[row * 2][col * 2]

    def bottom_left_vertex(self, col, row):
        return self._matrix[row * 2 + 2][col * 2]

    def top_right_vertex(self, col, row):
        return self._matrix[row * 2][col * 2 + 2]

    def bottom_right_vertex(self, col, row):
        return self._matrix[row * 2 + 2][col * 2 + 2]

    @property
    def most_left_card(self):
        return self.most_left_move.card

    @property
    def most_right_card(self):
        return self.most_right_move.card

    @property
    def top_card(self):
        return self.top_move.card

    @property
    def bottom_card(self):
        return self.bottom_move.card

    def dock_count(self, col, row):
        result = self.top_edge(col, row).dock_count + \
                 self.bottom_edge(col, row).dock_count + \
                 self.left_edge(col, row).dock_count + \
                 self.right_edge(col, row).dock_count + \
                 self.top_left_vertex(col, row).dock_count + \
                 self.top_right_vertex(col, row).dock_count + \
                 self.bottom_left_vertex(col, row).dock_count + \
                 self.bottom_right_vertex(col, row).dock_count
        return result

    def mandatory_dock_count(self, col, row):
        result = self.top_edge(col, row).mandatory_dock_count + \
                 self.bottom_edge(col, row).mandatory_dock_count + \
                 self.left_edge(col, row).mandatory_dock_count + \
                 self.right_edge(col, row).mandatory_dock_count + \
                 self.top_left_vertex(col, row).mandatory_dock_count + \
                 self.top_right_vertex(col, row).mandatory_dock_count + \
                 self.bottom_left_vertex(col, row).mandatory_dock_count + \
                 self.bottom_right_vertex(col, row).mandatory_dock_count
        return result

    def have_adjacent_card(self, col, row):
        up = self.top_square(col, row)
        down = self.bottom_square(col, row)
        left = self.left_square(col, row)
        right = self.right_square(col, row)
        return up.has_card or down.has_card or left.has_card or right.has_card

    def move_card(self, move):
        self.put_card(move.col, move.row, move.card)

    def put_card(self, col, row, card):
        self.square_at(col, row).has_card = True
        self.top_left_vertex(col, row).update(card.vertex(card.TOP_LEFT_VERTEX))
        self.top_right_vertex(col, row).update(card.vertex(card.TOP_RIGHT_VERTEX))
        self.bottom_left_vertex(col, row).update(card.vertex(card.BOTTOM_LEFT_VERTEX))
        self.bottom_right_vertex(col, row).update(card.vertex(card.BOTTOM_RIGHT_VERTEX))
        self.top_edge(col, row).update(card.vertex(card.TOP_EDGE))
        self.bottom_edge(col, row).update(card.vertex(card.BOTTOM_EDGE))
        self.left_edge(col, row).update(card.vertex(card.LEFT_EDGE))
        self.right_edge(col, row).update(card.vertex(card.RIGHT_EDGE))
        self._contact_count = \
            self.top_edge(col, row).contact_number + \
            self.bottom_edge(col, row).contact_number + \
            self.left_edge(col, row).contact_number + \
            self.right_edge(col, row).contact_number + \
            self.top_left_vertex(col, row).contact_number + \
            self.top_right_vertex(col, row).contact_number + \
            self.bottom_left_vertex(col, row).contact_number + \
            self.bottom_right_vertex(col, row).contact_number
        move = Move(col, row, card)
        self._move_history.append(move)
        self.update_extreme_cards(move)
        return self._contact_count

    def match(self, col, row, card):
        match = \
            self.top_left_vertex(col, row).match(card.vertex(card.TOP_LEFT_VERTEX)) and \
            self.top_right_vertex(col, row).match(card.vertex(card.TOP_RIGHT_VERTEX)) and \
            self.bottom_left_vertex(col, row).match(card.vertex(card.BOTTOM_LEFT_VERTEX)) and \
            self.bottom_right_vertex(col, row).match(card.vertex(card.BOTTOM_RIGHT_VERTEX)) and \
            self.top_edge(col, row).match(card.vertex(card.TOP_EDGE)) and \
            self.bottom_edge(col, row).match(card.vertex(card.BOTTOM_EDGE)) and \
            self.left_edge(col, row).match(card.vertex(card.LEFT_EDGE)) and \
            self.right_edge(col, row).match(card.vertex(card.RIGHT_EDGE))
        if not match:
            self._contact_count = 0
            return False
        self._contact_count = \
            self.top_edge(col, row).contact_number + \
            self.bottom_edge(col, row).contact_number + \
            self.left_edge(col, row).contact_number + \
            self.right_edge(col, row).contact_number + \
            self.top_left_vertex(col, row).contact_number + \
            self.top_right_vertex(col, row).contact_number + \
            self.bottom_left_vertex(col, row).contact_number + \
            self.bottom_right_vertex(col, row).contact_number
        return self._contact_count > 0

    def try_move(self, move):
        return not self.square_at(move.col, move.row).has_card and \
            self.have_adjacent_card(move.col, move.row) and \
            self.match(move.col, move.row, move.card)

    def play_card(self, col, row, card):
        if not self.square_at(col, row).has_card and \
               self.have_adjacent_card(col, row) and \
               self.match(col, row, card):
            self.put_card(col, row, card)
            card.played = True
        return True

    def update_extreme_cards(self, move):
        if len(self._move_history) == 1:
            self._most_right_move = move
            self._most_left_move = move
            self._top_move = move
            self._bottom_move = move
        else:
            if move.col > self._most_right_move.col:
                self._most_right_move = move
            if move.col < self._most_left_move.col:
                self._most_left_move = move
            if move.row < self._top_move:           # NO using GL coord system
                self._top_move = move
            if move.row > self._bottom_move:        # NO using GL coord system
                self._bottom_move = move
