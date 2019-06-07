from __future__ import division, print_function, unicode_literals

import pyglet
from tiles import *

__all__ = ['Player', 'HumanPlayer']


class Player(pyglet.event.EventDispatcher):
    def __init__(self, name):
        self.name = name
        self.cards = list()

    def add_card(self, card):
        self.cards.append(card)
        self.dispatch_event('on_card_add', card)

    def remove_card(self, card):
        self.cards.remove(card)
        self.dispatch_event('on_card_remove', card)

    def sort_cards_by_position(self):
        self.cards.sort(key = lambda card: card.x)

    def show_cards(self):
        for c in self.cards:
            c.set_state(CardState.FACE_UP)

    def hide_cards(self):
        for c in self.cards:
            c.set_state(CardState.UPSIDE_DOWN)

    def play(self):
        pass




class HumanPlayer(Player):
    pass


class RobotPlayer(Player):
    pass


Player.register_event_type('on_card_add')
Player.register_event_type('on_card_remove')
