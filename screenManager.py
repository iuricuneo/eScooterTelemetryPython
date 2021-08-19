import kivy
kivy.require('1.10.0')

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

from kivy.lang import Builder
buildKV = Builder.load_string("#:include main.kv")

from kivy.uix.screenmanager import ScreenManager, NoTransition

from screens.mainScreen import main_screen
from screens.homeScreen import home_screen
from screens.settingsScreen import settings_screen

sm = ScreenManager(transition=NoTransition())
sm.add_widget(home_screen)
sm.add_widget(main_screen)
sm.add_widget(settings_screen)
