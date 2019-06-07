
from cocos.sprite import Sprite
from cocos.rect import Rect
from cocos.tiles import *
from model import *

__all__ = ['CardState', 'Card']


class CardState:
    FACE_UP = 'Face up'
    UPSIDE_DOWN = 'Upside down'


class Card(Sprite, Tile):

    ALPHA_BASE = "ABCDEFGHIJSLOMNP"
    ALPHA_ROTE = "EFGHIJSLOMNPABCD"

    TOP_EDGE = 0
    BOTTOM_EDGE = 1
    LEFT_EDGE = 2
    RIGHT_EDGE = 3
    TOP_LEFT_VERTEX = 0
    TOP_RIGHT_VERTEX = 1
    BOTTOM_LEFT_VERTEX = 2
    BOTTOM_RIGHT_VERTEX = 3

    def __init__(self, name, state=CardState.FACE_UP):
        image = pyglet.image.load('res/textures/wood3.png')
        Sprite.__init__(self, image)
        Tile.__init__(self, name, None, image)
        # super(Card, self).__init__('res/textures/fabric11.png')
        # super(Card, self).__init__('res/textures/grass5.png')
        file_name = 'res/graphes/' + name
        self.graphe = Sprite(file_name)
        self.add(self.graphe)
        self._state = self.set_state(state)
        self._name = name
        self._played = False
        self._edge = [None, None, None, None]
        self._vertex = [None, None, None, None]

    @property
    def played(self):
        return self._played

    @played.setter
    def played(self, val):
        self._played = val

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        self.find_vertex(self.TOP_LEFT_VERTEX, "E")
        self.find_vertex(self.TOP_RIGHT_VERTEX, "I")
        self.find_vertex(self.BOTTOM_LEFT_VERTEX, "A")
        self.find_vertex(self.BOTTOM_RIGHT_VERTEX, "O")
        self.find_edge(self.TOP_EDGE, "FGH")
        self.find_edge(self.BOTTOM_EDGE, "PNM")
        self.find_edge(self.LEFT_EDGE, "DCB")
        self.find_edge(self.RIGHT_EDGE, "JSL")

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        if state == CardState.FACE_UP:
            self.graphe.visible = True
        else:
            self.graphe.visible = False
        return state

    def find_vertex(self, index, char):
        k = self._name.find(char)
        v = Vertex()
        if k == -1:
            v.state = State.CLOSED
        elif k == 1:
            v.state = State.OPTIONAL
        else:
            v.state = State.MANDATORY
        self._vertex[index] = v

    def find_edge(self, index, char):
        e = Edge()
        for i in range(3):
            k = self._name.find(char[i])
            if k == -1:
                e.port[i] = State.CLOSED
            elif k == 1:
                e.port[i] = State.OPTIONAL
            else:
                e.port[i] = State.MANDATORY
        self._edge[index] = e

    def edge(self, index):
        return self._edge[index]

    def vertex(self, index):
        return self._vertex[index]

    def has_point(self, x, y):
        px, py = self.position
        px -= self.width // 2
        py -= self.height // 2
        r = Rect(px, py, self.width, self.height)
        return r.contains(x, y)

    def rotate_clock_wise(self):
        new_name = ''
        for i in range(3):
            new_name += self.ALPHA_ROTE[self.ALPHA_BASE.find(self._name[i])]
        self.set_name(new_name)
        self.graphe.rotation += 90
        if self.graphe.rotation == 360:
            self.graphe.rotation = 0

    def rotate_counter_clock_wise(self):
        new_name = ''
        for i in range(3):
            new_name += self.ALPHA_BASE[self.ALPHA_ROTE.find(self._name[i])]
        self.set_name(new_name)
        self.graphe.rotation -= 90
        if self.graphe.rotation == 360:
            self.graphe.rotation = 0
