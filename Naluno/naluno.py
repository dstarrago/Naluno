
from __future__ import division, print_function, unicode_literals

import pyglet
pyglet.options['shadow_window'] = False

from pyglet import font
from pyglet import gl
from pyglet.window import key

import cocos
from cocos.layer import *
from cocos.scene import Scene
from cocos.scenes.transitions import *
from cocos.actions.instant_actions import *
from cocos.actions import *
from cocos.sprite import *
from cocos.menu import *
from cocos.text import *

from HUD import BackgroundLayer


class MainMenu(Menu):

    def __init__(self):
        super( MainMenu, self).__init__('CONTACT')

        # you can override the font that will be used for the title and the items
        # you can also override the font size and the colors. see menu.py for
        # more info
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Bauhaus 93',
        self.font_item['color'] = (32,16,32,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['color'] = (32,16,32,255)
        self.font_item_selected['font_size'] = 46

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = CENTER
        self.menu_anchor_x = CENTER

        items = []

        items.append(MenuItem('Individual Game', self.on_new_allvsall_game))
        items.append(MenuItem('Team Game', self.on_team_mode_game))
        items.append(MenuItem('Options', self.on_options))
        items.append(MenuItem('Hall of Fame', self.on_scores))
        items.append(MenuItem('Quit', self.on_quit))

        self.create_menu( items, shake(), shake_back() )

    def on_new_allvsall_game(self):
        pass
        # import gameview
        # director.push( FlipAngular3DTransition(
        #     gameview.get_newgame(), 1.5 ) )

    def on_team_mode_game(self):
        import view_2p
        director.push(FlipAngular3DTransition(view_2p.team_mode_game(), 1.5))

    def on_options( self ):
        pass
        # self.parent.switch_to(1)

    def on_scores( self ):
        pass
        # self.parent.switch_to(2)

    def on_quit(self):
        pyglet.app.exit()


class OptionsMenu( Menu ):
    def __init__(self):
        super( OptionsMenu, self).__init__('ROADS')

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Bauhaus 93',
        self.font_item['color'] = (32,16,32,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['color'] = (32,16,32,255)
        self.font_item_selected['font_size'] = 46

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = CENTER
        self.menu_anchor_x = CENTER

        items = []

        # items.append( MultipleMenuItem(
        #                 'SFX volume: ',
        #                 self.on_sfx_volume,
        #                 self.volumes,
        #                 int(soundex.sound_vol * 10) )
        #             )
        # items.append( MultipleMenuItem(
        #                 'Music volume: ',
        #                 self.on_music_volume,
        #                 self.volumes,
        #                 int(soundex.music_player.volume * 10) )
        #             )
        items.append( ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS) )
        items.append( MenuItem('Fullscreen', self.on_fullscreen) )
        items.append( MenuItem('Back', self.on_quit) )
        self.create_menu( items, shake(), shake_back() )

    def on_fullscreen( self ):
        director.window.set_fullscreen( not director.window.fullscreen )

    def on_quit( self ):
        self.parent.switch_to( 0 )

    def on_show_fps( self, value ):
        director.show_FPS = value


def main():
    pyglet.resource.path.append('res')
    pyglet.resource.reindex()

    font.add_directory('res')
    from cocos.director import director
    director.init(fullscreen=True)

    scene = Scene()
    scene.add(MultiplexLayer(
                    MainMenu(),
                    OptionsMenu(),
                    ),
              z=1)
    scene.add(BackgroundLayer(), z=0)
    director.run(scene)


if __name__ == '__main__':
    main()
