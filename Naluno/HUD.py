from __future__ import division, print_function, unicode_literals

import os
# This code is so you can run the samples without installing the package
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from cocos.layer import *
from cocos.sprite import Sprite
from cocos.director import director


class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.bg = Sprite('backgrounds/roads14.jpg')
        self.add(self.bg)
        w, h = director.get_window_size()
        ratio = w / self.bg.width
        self.bg.scale = ratio
        self.bg.position = (w // 2, h // 2)
