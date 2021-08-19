import kivy
kivy.require('1.10.0')

from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty

from screens.mainScreen import main_screen

class SettingsScreen(Screen):

    #
    # This screen has controls for settings such as color changes, show states,
    # etc. The data is saved and loaded from a file called "settings.config"
    # and if the file is not found, will return an error.
    #

    settings = {
        'graphXAxis' : 1000,
        'sizeYGraph' : 0.6,
        'speedColor' : True,
        'battColor' : True,
        'lipoColor' : True,
        'incColor' : True,
        'stateImg' : True,
        'dataToServer' : True,
        'timeToSend' : 0.5 }

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self._load_settings()

    def _load_settings(self):

        # Internal fuction responsible for reading from file and applying
        # the necessary changes.

        # Reads data from file.

        try:

            with open('settings.config', 'r') as f:
                content = f.readlines()
                f.close()
            content = [x.strip().split('=') for x in content]

            for i in content:
                if i[1] == 'True':
                    self.settings[i[0]] = True
                elif i[1] == 'False':
                    self.settings[i[0]] = False
                elif i[0] == 'sizeYGraph':
                    self.settings[i[0]] = float(i[1])
                elif i[0] == 'graphXAxis':
                    self.settings[i[0]] = int(i[1])
                elif i[0] == 'timeToSend':
                    self.settings[i[0]] = float(i[1])

        except:
            print('Config file \'settings.config\' not found')
            pass

        # Update controls to loaded data
        try:
            self.ids.speedcolor.active = self.settings['speedColor']
            self.ids.battcolor.active = self.settings['battColor']
            self.ids.lipocolor.active = self.settings['lipoColor']
            self.ids.inccolor.active = self.settings['incColor']
            self.ids.stateimg.active = self.settings['stateImg']
            self.ids.dataserver.active = self.settings['dataToServer']
            self.ids.timesend.text = str(self.settings['timeToSend'])
            self.ids.graphsamples.text = str(self.settings['graphXAxis'])

            if self.settings['sizeYGraph'] > 0:
                self.ids.showgraph.active = True
            else:
                self.ids.showgraph.active = False

            # Send loaded data to mainScreen settings
            for i in self.settings.keys():
                main_screen.settings[i] = self.settings[i]

            # Updates mainScreen content to loaded settings
            main_screen.state = './img/transparency.png'

            main_screen.graph.xmax = main_screen.settings['graphXAxis']
            main_screen.graph.size_hint_y = main_screen.settings['sizeYGraph']

            if main_screen.settings['sizeYGraph'] == 0:
                main_screen.ids.speedlabel.font_size = 60
                main_screen.ids.speedlabel.pos_hint = { 'x': -0.1 , 'y': 0 }
            else:
                main_screen.ids.speedlabel.font_size = 40
                main_screen.ids.speedlabel.pos_hint = { 'x': -.3 , 'y': -.35 }

        except Exception as e:
            print(e)
            self.manager.current = 'home'

    def save_settings(self):
        # Writes data to file
        try:
            self.settings['graphXAxis'] = int(self.ids.graphsamples.text)
            self.settings['timeToSend'] = float(self.ids.timesend.text)
        except:
            print('Value entered is not a number')
            return

        with open('settings.config', 'w') as f:
            for i in self.settings.keys():
                f.write( i + '=' + str(self.settings[i])+'\n')
            f.close()

        # Writes data to mainScreen settings
        for i in self.settings.keys():
            main_screen.settings[i] = self.settings[i]

        # Apply changes to mainScreen content
        main_screen.state = './img/transparency.png'

        main_screen.graph.xmax = main_screen.settings['graphXAxis']
        main_screen.graph.size_hint_y = main_screen.settings['sizeYGraph']

        if main_screen.settings['sizeYGraph'] == 0:
            main_screen.ids.speedlabel.font_size = 60
            main_screen.ids.speedlabel.pos_hint = { 'x': -0.1 , 'y': 0 }
        else:
            main_screen.ids.speedlabel.font_size = 40
            main_screen.ids.speedlabel.pos_hint = { 'x': -.3 , 'y': -.35 }

    def back_from_settings(self):
        # Function to return to home from settings. Will save and return
        self.save_settings()
        self.manager.current = 'home'

    def save_and_close(self, *kwargs):
        # Function to save and close app. Callback of modal "ja" button
        self.save_settings()
        self.close_app()

    def close_app(self, *kwargs):
        # Closes app
        from kivy.app import App as app

        app.get_running_app().stop()

    # Control/switch callbacks
    def speed_color(self, instance, value):
        self.settings['speedColor'] = value

    def batt_color(self, instance, value):
        self.settings['battColor'] = value

    def lipo_color(self, instance, value):
        self.settings['lipoColor'] = value

    def inc_color(self, instance, value):
        self.settings['incColor'] = value

    def state_img(self, instance, value):
        self.settings['stateImg'] = value

    def data_server(self, instance, value):
        self.settings['dataToServer'] = value

    def show_graph(self, instance, value):
        if not value:
            self.settings['sizeYGraph'] = 0
        else:
            self.settings['sizeYGraph'] = 0.6

    def open_modal(self):
        # Opens modal before closing app, to know whether user wants to save
        # changes, don't save, or cancel
        from kivy.uix.modalview import ModalView
        from kivy.uix.button import Button
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.label import Label
        from kivy.graphics.instructions import InstructionGroup
        from kivy.graphics.context_instructions import Color
        from kivy.graphics.vertex_instructions import Rectangle

        view = ModalView(size_hint=(None, None), size=(400,100))

        save = Button(text='Ja', on_press=self.save_and_close,
                      pos_hint={'x':.0625, 'y':.2}, size_hint=(.25,.35))

        dontsave = Button(text='Nein', on_press=self.close_app,
                          pos_hint={'x':.375, 'y':.2}, size_hint=(.25,.35))

        cancel = Button(text='Abbrechen', on_press=view.dismiss,
                          pos_hint={'x':.6975, 'y':.2}, size_hint=(.25,.35))

        label = Label(text='Moechten Sie die Aenderungen speichern?',
                      size_hint=(1,.4), pos_hint={'x':0, 'y':.55},
                      color=[1,1,1,1])

        layout = FloatLayout()

        layout.add_widget(save)
        layout.add_widget(dontsave)
        layout.add_widget(cancel)
        layout.add_widget(label)

        view.add_widget(layout)

        view.open()

    pass

settings_screen = SettingsScreen(name='settings')
