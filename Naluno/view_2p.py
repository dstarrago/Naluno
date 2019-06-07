from cocos.tiles import RectMapLayer
from cocos.rect import Rect
from config import *
import cocos
from cocos.scene import Scene
from cocos import layer
from cocos.text import *
from cocos.director import director
from cocos.sprite import Sprite

from game import *
from gamectrl import *

__all__ = ['PlayerPosition', 'team_mode_game', 'individual_mode_game']


class Table(RectMapLayer):
    def __init__(self, cells, properties=None):
        super(Table, self).__init__(0, HOR_MAP_SIZE, VER_MAP_SIZE, cells, None, properties)
        background = layer.util_layers.ColorLayer(107, 142, 35, 255)      # Olive Drab
        # background = ColorLayer(95, 158, 160, 255)    # Cadet Blue
        # background = ColorLayer(205, 133, 63, 255)    # Peru
        # background = ColorLayer(139, 69, 19, 255)     # Saddle Brown
        self.add(background)


class PlayerPane(layer.Layer):
    CARD_SPACE = 4

    def __init__(self, player):
        super(PlayerPane, self).__init__()
        self._player = player
        self._player.push_handlers(self.on_card_add,
                                   self.on_card_remove
                                   )

    @property
    def player(self):
        return self._player

    def on_card_add(self, card):
        self.add(card)

    def on_card_remove(self, card):
        self.remove(card)

    def update_card_positions(self):
        pass


class MainPlayerPane(PlayerPane):

    # is_event_handler = True #: enable pyglet's events
    CARD_SPACE = 4
    BANNER_MARGIN = 0

    def __init__(self, player):
        super(MainPlayerPane, self).__init__(player)
        self.dragged = None
        self._banner = Sprite('res/banners/banner1.png')  # DarkStitch
        self._banner.opacity = 180
        self._banner.scale_x = 0.8
        self._banner.scale_y = 1.2
        self.banner_offset_y = 0
        self.add(self._banner)
        w, h = director.get_window_size()
        self._banner.position = w // 2, self._banner.height // 2 + 10
        self.player_name = Label(self._player.name, font_size=22,
                                 font_name='Bradley Hand ITC',
                                 color=(255, 255, 255, 255),
                                 anchor_x='left',
                                 anchor_y='center')
        self.player_name.position=(self._banner.x + self._banner.width // 2,
                                   self._banner.y)
        self.add(self.player_name)

    @property
    def banner(self):
        return self._banner

    def refine_card_positions(self):
        self._player.sort_cards_by_position()
        self.update_card_positions()

    def update_card_positions(self):
        gap = (card_size * (len(self._player.cards) - 1) +
               self.CARD_SPACE * (len(self._player.cards) - 1)) // 2
        ox = 0
        for c in self._player.cards:
            c.position = self._banner.x + (c.width + self.CARD_SPACE) * ox - gap, \
                         self._banner.y + self.banner_offset_y
            ox += 1


class PlayerPosition:
    TOP = 'top'
    LEFT = 'left'
    RIGHT = 'right'


class OtherPlayerPane(PlayerPane):

    def __init__(self, player, side=PlayerPosition.TOP):
        super(OtherPlayerPane, self).__init__(player)
        self.side = side
        self.banner = Sprite('res/banners/banner1.png')  # DarkStitch
        w, h = director.get_window_size()
        if self.side == PlayerPosition.LEFT:
            self.banner.opacity = 180
            self.banner.scale_x = 0.8
            self.banner.scale_y = 1.2
            self.banner.rotation = 90
            self.banner_offset_x = 0
            self.banner_offset_y = 0
            self.banner.position = self.banner.height // 2 + 10, h // 2
            self.player_name = Label(self._player.name, font_size=22,
                                     font_name='Bradley Hand ITC',
                                     color=(255, 255, 255, 255),
                                     anchor_x='center',
                                     anchor_y='top')
            self.player_name.position = (self.banner.x + 20,
                                         self.banner.y - self.banner.width // 2)
            self.add(self.player_name)
        elif self.side == PlayerPosition.TOP:
            self.banner.opacity = 180
            self.banner.scale_x = 0.8
            self.banner.scale_y = 1.2
            self.banner_offset_y = 0
            self.banner.rotation = 180
            self.banner.position = w // 2, h - self.banner.height // 2 - 10
            self.player_name = Label(self._player.name, font_size=22,
                                     font_name='Bradley Hand ITC',
                                     color=(255, 255, 255, 255),
                                     anchor_x='right',
                                     anchor_y='center')
            self.player_name.position = (self.banner.x - self.banner.width // 2,
                                         self.banner.y)
            self.add(self.player_name)
        else:
            self.banner.opacity = 180
            self.banner.scale_x = 0.8
            self.banner.scale_y = 1.2
            self.banner_offset_y = 0
            self.banner.rotation = 270
            self.banner_offset_x = 0
            self.banner.position = w - self.banner.height // 2 - 10, h // 2
            self.player_name = Label(self._player.name, font_size=22,
                                     font_name='Bradley Hand ITC',
                                     color=(255, 255, 255, 255),
                                     anchor_x='center',
                                     anchor_y='bottom')
            self.player_name.position = (self.banner.x - 20,
                                         self.banner.y + self.banner.width // 2)
            self.add(self.player_name)
        self.add(self.banner)

    def update_card_positions(self):
        if self.side == PlayerPosition.TOP:
            self.update_top_position()
        elif self.side == PlayerPosition.LEFT:
            self.update_left_position()
        else:
            self.update_right_position()

    def update_top_position(self):
        gap = (card_size * (len(self._player.cards) - 1) +
               self.CARD_SPACE * (len(self._player.cards) - 1)) // 2
        ox = 0
        for c in self._player.cards:
            c.position = self.banner.x + (c.width + self.CARD_SPACE) * ox - gap, \
                         self.banner.y + self.banner_offset_y
            ox += 1

    def update_left_position(self):
        gap = (card_size * (len(self._player.cards) - 1) +
               self.CARD_SPACE * (len(self._player.cards) - 1)) // 2
        oy = 0
        for c in self._player.cards:
            c.position = self.banner.x + self.banner_offset_x, \
                         self.banner.y - gap + (c.width + self.CARD_SPACE) * oy + self.banner_offset_y
            oy += 1

    def update_right_position(self):
        gap = (card_size * (len(self._player.cards) - 1) +
               self.CARD_SPACE * (len(self._player.cards) - 1)) // 2
        oy = 0
        for c in self._player.cards:
            c.position = self.banner.x + self.banner_offset_x, \
                         self.banner.y - gap + (c.width + self.CARD_SPACE) * oy + self.banner_offset_y
            oy += 1

def team_mode_game():
    """returns the game scene"""
    scene = Scene()
    game = Game()
    table = RectMapLayer('Table', HOR_MAP_SIZE, VER_MAP_SIZE, game.cells, origin=(0, 0, 0))
    table.debug = True
    player = MainPlayerPane(game.players[0])
    adversary1 = OtherPlayerPane(game.players[1], PlayerPosition.LEFT)
    adversary2 = OtherPlayerPane(game.players[2], PlayerPosition.RIGHT)
    adversary3 = OtherPlayerPane(game.players[3], PlayerPosition.TOP)

    game.deal_cards()
    game.players[0].show_cards()

    player.update_card_positions()
    adversary1.update_card_positions()
    adversary2.update_card_positions()
    adversary3.update_card_positions()

    background = layer.util_layers.ColorLayer(107, 142, 35, 255)
    background.add(player, z=3, name='player area')
    background.add(adversary1, z=4, name='adversary 1')
    background.add(adversary2, z=5, name='adversary 2')
    background.add(adversary3, z=6, name='adversary 3')

    # im = pyglet.image.load('res/textures/wood3.png')
    # for i in range(HOR_MAP_SIZE):
    #     for j in range(VER_MAP_SIZE):
    #         s = Sprite(im)
    #         background.add(s, z=1)
    #         s.position = table.cells[i][j].center

    scroller = layer.ScrollingManager()
    scroller.add(table, z=2, name='table')
    fx = card_size * HOR_MAP_SIZE//2
    fy = card_size * VER_MAP_SIZE//2
    scroller.set_focus(fx, fy, True)

    ctrl = GameCtrl(game, player, table, scroller)

    scene.add(background, z=0, name='background')
    scene.add(ctrl, z=7, name='controller')
    scene.add(scroller, z=8, name='scroller')
    # scene.add(player, z=3, name='player area')
    # scene.add(adversary1, z=4, name='adversary 1')
    # scene.add(adversary2, z=5, name='adversary 2')
    # scene.add(adversary3, z=6, name='adversary 3')

    return scene


def individual_mode_game():
    pass
