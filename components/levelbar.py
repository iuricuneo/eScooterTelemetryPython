import kivy

kivy.require('1.10.0')

from kivy.app import App

from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import ReferenceListProperty

from kivy.utils import get_color_from_hex

from kivy.graphics import Color, Rectangle

__all__ = ('LevelBar',)

__title__ = 'levelbar'
__version__ = '1'
__author__ = 'me'

class LevelBar(Widget):
    '''
    Creates a vertical progress bar, with a 3px border.
    Accepts color changes for border, background and the fill bar. Colors are
    expected in 6 hex digits format, with a # in front, as in '#123abc'
    Receives a max parameter, min is fixed to 0.
    Value parameter will tell how high the bar should fill. this parameter is
    bounded between 'max' and zero.
    '''

    max = NumericProperty(100)
    value = NumericProperty(50)

    border_color = StringProperty('#000000')
    bg_color = StringProperty('#ffffff')
    fill_color = StringProperty('#000000')

    def __init__(self, **kwargs):

        super(LevelBar, self).__init__(**kwargs)

        # Creates the drawing
        self._draw_elements()

        # Adds widgets to canvases
        self._add_widgets()

        # Binds changes in attributes to redraw necessary canvases
        self.bind( border_color=self._update,
                   bg_color=self._update,
                   fill_color=self._update,
                   pos=self._update,
                   size=self._update )

        self.bind( value=self._draw_fill_bar,
                   max=self._draw_fill_bar )

    def _update(self, *args):

        # Redraws canvas to show changes

        # Delete current canvases
        self._inner_layout.remove_widget(self._fill_bar)
        self._layout.remove_widget(self._inner_layout)
        self.remove_widget(self._layout)

        # Create new canvases
        self._draw_elements()
        self._add_widgets()

        # Adjust fill bar height
        self._draw_fill_bar()

    def _draw_fill_bar(self, *args):

        # Redraws fill bar to adjust height

        # Bounds value
        if self.value > self.max:
            self.value = self.max
        elif self.value < 0:
            self.value = 0

        # Delete current canvas
        self._inner_layout.remove_widget(self._fill_bar)

        # Get new height
        tmp = (self.size[1] - 6)
        tmp *= self.value/self.max

        # Create new canvas

        self._fill_bar = FloatLayout( size=(self.size[0] - 6, int(tmp)))

        tmpR = '0x' + self.fill_color[1:3]
        tmpG = '0x' + self.fill_color[3:5]
        tmpB = '0x' + self.fill_color[5:7]

        with self._fill_bar.canvas:
            Color( int(tmpR, 0)/255, int(tmpG, 0)/255, int(tmpB, 0)/255 )
            self.fill_rect = Rectangle( size=self._fill_bar.size,
                                        pos=(self.pos[0]+3, self.pos[1]+3) )

        # Add new canvas
        self._inner_layout.add_widget(self._fill_bar)

    def _draw_elements(self):

        # Creates canvases

        # External canvas for border
        self._layout = FloatLayout()

        tmpR = '0x' + self.border_color[1:3]
        tmpG = '0x' + self.border_color[3:5]
        tmpB = '0x' + self.border_color[5:7]

        with self._layout.canvas:
            Color( int(tmpR, 0)/255, int(tmpG, 0)/255, int(tmpB, 0)/255 )
            self.border_rect = Rectangle(size=self.size, pos=self.pos)

        # Inner canvas for background
        self._inner_layout = FloatLayout()

        tmpR = '0x' + self.bg_color[1:3]
        tmpG = '0x' + self.bg_color[3:5]
        tmpB = '0x' + self.bg_color[5:7]

        with self._inner_layout.canvas:
            Color( int(tmpR, 0)/255, int(tmpG, 0)/255, int(tmpB, 0)/255 )
            self.bg_rect = Rectangle( size=(self.size[0]-6, self.size[1]-6),
                                      pos=(self.pos[0]+3, self.pos[1]+3) )

        # Fill bar to show value. Will be redrawn
        self._fill_bar = FloatLayout()

        tmpR = '0x' + self.fill_color[1:3]
        tmpG = '0x' + self.fill_color[3:5]
        tmpB = '0x' + self.fill_color[5:7]

        with self._fill_bar.canvas:
            Color( int(tmpR, 0)/255, int(tmpG, 0)/255, int(tmpB, 0)/255 )
            self.fill_rect = Rectangle(size=self.size, pos=self.pos)

    def _add_widgets(self):

        # Adds canvases to correct parents

        self._inner_layout.add_widget(self._fill_bar)
        self._layout.add_widget(self._inner_layout)
        self.add_widget(self._layout)

if __name__ == '__main__':
    from kivy.uix.slider import Slider
    from kivy.uix.boxlayout import BoxLayout

    class LevelBarApp(App):

        def build(self):

            # Creates layout
            box = BoxLayout(orientation='horizontal', padding=5)

            # Creates level bar component
            self.levelbar = LevelBar( max=10,
                                      value=0,
                                      fill_color='#d6d640',    #yellow
                                      bg_color='#87b2a9',      #grey-ish blue
                                      border_color='#552f6b' ) #purple

            # Creates control for level bar's value
            self.stepper = Slider(min=0, max=10)
            # Binds function to change level bar's value when slider's value
            # changes
            self.stepper.bind(value=self.update_level)

            # Adds level bar to layout
            box.add_widget(self.levelbar)
            # Adds slider to layout
            box.add_widget(self.stepper)

            # Returns layout to create app
            return box

        def update_level(self, *args):
            # Callback to change level bar's value from slider change
            self.levelbar.value = self.stepper.value

    LevelBarApp().run()
