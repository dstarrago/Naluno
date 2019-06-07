import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from config import *

# stdlib
import copy
import random

# pyglet related
import pyglet
from pyglet.window import key

# cocos2d related
from cocos.layer import *
from cocos.scene import Scene
from cocos.euclid import Point2
from cocos.director import director
from cocos.tiles import RectMap
from cocos.tiles import RectCell

__all__ = ['GameCtrl']

#
# Controller ( MVC )
#


class GameCtrl(Layer):

    is_event_handler = True #: enable pyglet's events

    def __init__(self, game, player_pane, table, scroller):
        Layer.__init__(self)
        self._game = game
        self._cells = game.cells
        self._map = game.map
        self._player_pane = player_pane
        self._table = table
        self.scroller = scroller
        self._dragged = None
        self.prev_x = 0
        self.prev_y = 0

    @property
    def game(self):
        return self._game

    @property
    def cells(self):
        return self._cells

    @property
    def map(self):
        return self._map

    @property
    def player_pane(self):
        return self._player_pane

    @property
    def table(self):
        return self._table

    @property
    def background(self):
        return self._table

    def on_mouse_release(self, x, y, button, modifiers):
        if self._dragged:
            if y > self.player_pane.banner.get_rect().top:
                if self.game.new_game:
                    cell = self.game.cells[HOR_MAP_SIZE // 2][VER_MAP_SIZE // 2]
                else:
                    cell = self.table.get_at_pixel(x, y)
                if cell is None:
                    self._dragged.position = self.prev_x, self.prev_y
                else:
                    self.player_pane.remove(self._dragged)
                    self.table.add(self._dragged, z=1)
                    self._dragged.position = cell.center
                    fx, fy = cell.center
                    self.scroller.set_focus(fx, fy)
                    print('card center: ', self._dragged.get_rect().center)
            else:
                self.player_pane.refine_card_positions()
            self._dragged = None
        else:
            for c in self.player_pane.player.cards:
                if c.has_point(x, y):
                    c.rotate_clock_wise()
                    break

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._dragged:
            fx, fy = self._dragged.position
            self._dragged.set_position(fx + dx, fy + dy)
        else:
            for c in self._player_pane.player.cards:
                if c.has_point(x, y):
                    self._dragged = c
                    self.prev_x, self.prev_y = c.position
                    self.player_pane.remove(self._dragged)
                    self.player_pane.add(self._dragged, z=1)
                    fx, fy = self._dragged.position
                    self._dragged.set_position(fx + dx, fy + dy)
                    break


