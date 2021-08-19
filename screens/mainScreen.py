import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen

from components.graph import Graph, SmoothLinePlot
from components.gauge import Gauge
from components.dataSet import DataSet as DS

from generalFunctions import read_serial, prepare_screen_change
from screens.homeScreen import home_screen

class MainScreen(Screen):

    # Main Screen

    ## Set volatile variables
    speed = StringProperty()
    batt = StringProperty(0)
    lipo = StringProperty(0)
    up_arrow = StringProperty()
    down_arrow = StringProperty()
    left_arrow = StringProperty()
    right_arrow = StringProperty()
    state = StringProperty()
    accel_state = StringProperty('#c8c8c8')
    signalImgCounter = NumericProperty(0)
    inclination = NumericProperty(50)
    increasing = NumericProperty(1)
    mode = StringProperty()

    counter = 0

    settings = {
        'sizeYGraph' : NumericProperty(1.3),
        'graphXAxis' : 1000,
        'speedColor' : True,
        'battColor' : True,
        'lipoColor' : True,
        'incColor' : True,
        'stateImg' : True,
        'dataToServer' : True,
        'timeToSend' : 0.5 }

    dataToServer = {
        "speed": "0",
        "batt": "0",
        "lipo": "0",
        "inclination": "0",
        "state": "0",
        "mode": "0",
        "accelState": "0",
        "inc": "0",
        "accel": "0"
    }

    # Number of messages until signal icon changes to no signal
    numMsgToNoSignal = 50                   # 1 second

    counterToUpdateServer = 0

    # Initializes dataSet for logging
    ds = DS()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        ## Initialize variables
        self.speed = str(0)
        self.batt = str(0)
        self.lipo = str(0)
        self.up_arrow = './img/white-up.png'
        self.down_arrow = './img/white-down.png'
        self.left_arrow = './img/white-left.png'
        self.right_arrow = './img/white-right.png'
        #self.state = './img/transparency.png'
        self.accel_state = '#c8c8c8'
        #self.mode = './img/transparency.png'
        self.state = './img/no_batt.png'
        self.mode = './img/sacurity_icon.png'

        self.counter = 0

        # Initialize diagram
        self.graph = self.ids.graph_plot
        self.plot = []
        self.plot.append(SmoothLinePlot(color=[0, 0, 0, 1]))
        self.reset_plots()

        for plot in self.plot:
            self.graph.add_plot(plot)

        self.gauge = self.ids.gauge

    def reset_plots(self):
        # Clear diagram
        for plot in self.plot:
            plot.points = [(0,0)]
        self.counter = 1

    def update_plot(self):

        # Updates diagram according to setting

        # If we have more data than we want, cut it short
        if len(self.plot[0].points) > self.settings['graphXAxis']:
            self.plot[0].points = self.plot[0].points[(-self.graph_x_axis):]

        # If we have already all points, shift array
        if self.counter >= self.settings['graphXAxis']:
            for plot in self.plot:
                del(plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]

            self.counter = self.settings['graphXAxis'] - 1

        # Limits speed to 3000w
        speed = int(self.speed) if int(self.speed) < 3000 else 3000

        # Add new datum
        self.plot[0].points.append( (self.counter, speed) )

        self.counter += 1

    ## Function to be called to return to HomeScreen.
    def stop_reading(self, *args):
        prepare_screen_change(self, home_screen)
        self.manager.current = 'home'

    ## Closes app.
    def close_app(self):
        prepare_screen_change(self, home_screen)
        App.get_running_app().stop()

    pass

# Creates instance of the class so that its attributes can be handled in other
# files
main_screen = MainScreen(name='main')
