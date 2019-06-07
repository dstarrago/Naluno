
import sys
import os
# from cards import *
from tiles import *
from players import *
from config import *
from model import *
from pathlib import Path
from cocos.tiles import RectCell


class Game:
    def __init__(self):
        self._cards = list()
        self._players = list()
        self._create_card_list()
        self._create_players()
        self._cells = [[RectCell(x, y, card_size, card_size, None, None)
                        for y in range(VER_MAP_SIZE)] for x in range(HOR_MAP_SIZE)]
        self._map = Map()

    @property
    def cards(self):
        return self._cards

    @property
    def players(self):
        return self._players

    @property
    def cells(self):
        return self._cells

    @property
    def map(self):
        return self._map

    @property
    def new_game(self):
        return len(self._map.move_history) == 0

    def _create_card_list(self):
        p = Path('res/graphes')
        for child in p.iterdir():
            if child.is_file():
                card = Card(str(child.name), state=CardState.UPSIDE_DOWN)
                # card.anchor = 0, 0
                self.cards.append(card)

    def _create_players(self):
        self.players.append(Player('Lola'))
        self.players.append(Player('Rafaela'))
        self.players.append(Player('Lelo'))
        self.players.append(Player('Bebo'))

    def deal_cards(self):
        c = 0
        for i in range(cards_per_player):
            for p in self.players:
                p.add_card(self.cards[c])
                c += 1


if __name__ == '__main__':
    pass
