from __future__ import division, print_function, unicode_literals

import pyglet
pyglet.options['shadow_window'] = False

import cocos
from cocos import tiles, actions, layer
from cocos.actions import *

def main():
    from cocos.director import director
    director.init(width=1200, height=600, autoscale=False, resizable=True)
    
    card_layer = layer.ScrollableLayer()
    cards = set()
    for i in range(9):
        card = cocos.sprite.Sprite('Resources/Box_Orange.png')
        card.scale = 1/3
        card.position = (-100, -100)
        cards.add(card)
        card_layer.add(card)
    
    ox = 0
    oy = 0
    t = 1
    for c in cards:
        c.do(Delay(t) + Accelerate(MoveTo((200 + ox, 200 + oy), duration=1)|RotateBy(720, 1), 3))
        if t in (3, 6):
            ox = 0
            oy += card.height
        else:
            ox += card.width
        t += 1

    main_scene = cocos.scene.Scene(card_layer)
    director.run(main_scene)
    

if __name__ == '__main__':
    main()
