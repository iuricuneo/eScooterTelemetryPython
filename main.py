# Software to receive data from eScooter via XBee modules.
# Consists of 2 screens, first responsible for allowing user to choose
# serial port and communication parameters. Second responsible for
# showing data received to user.
# --
# Technische Hochschule Ingolstadt.
# Labor fuer Mechatronik G005
# --
# Prof. Dr. Harald Goellinger
# Frau Karin Ebenbeck
# Herr Iuri Ferreira
# --
# Programmer:
# Iuri Cuneo Ferreira
# --
# All rights reserved.

from kivy import Config

Config.set('graphics', 'multisamples', 0)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

import os
import kivy
kivy.require('1.10.0')
from kivy.app import App


from kivy.factory import Factory
from components.levelbar import LevelBar
Factory.register('LevelBar', cls=LevelBar)

# Imports and runs the code from screen_manager

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

__location__ = __location__+'\screenManager.py'

externFile = open(__location__).read()

exec(compile(
    source=externFile,
    filename='screenManager.py',
    mode='exec'))

class eScooterTelemetry(App):
    def build(self):
        self.icon = 'logo.png'
        return sm

    def on_stop(self):

        from screens.mainScreen import main_screen as MS
        from screens.homeScreen import home_screen as HS

        if HS.dataLogging and MS.ds.File != None and not MS.ds.File.closed:
            MS.ds.close()

        if HS.serial != None and HS.serial.isOpen():
            #HS.serial.cancel_read()
            HS.serial.close()

if __name__ == '__main__':
    eScooterTelemetry().run()
