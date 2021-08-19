import kivy
kivy.require('1.10.0')

import serial

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from generalFunctions import ( get_serial_ports,
                                   read_serial,
                                   start_serial,
                                   saveFileDialog )

Timer_read_buffer = None
Timer_get_ports = None

class HomeScreen(Screen):

    # This screen is shown when the app starts.
    # Its attributes contain the chosen settings, the list of available ports,
    # the dropdown menu to choose a port, the timed functions
    # and the chosen port (or None)

    dropdown = DropDown()
    list_ports = ListProperty()
    dataLogging = BooleanProperty()
    chosen_port = StringProperty()
    fileName = StringProperty()
    filePath = StringProperty()
    chosen_baudrate = 9600
    chosen_stopbits = 1
    chosen_parity = 'N'
    chosen_bytesize = 8
    chosen_timeout = 0.02
    chosen_rtscts = 0
    serial = None
    Timer_get_ports = None
    Timer_read_buffer = None

    def __init__(self, **kwargs):

        # Will start setting the port reader, to get available ports.
        # Afterwards, gets available ports and generates the dropdown menu.

        super(HomeScreen, self).__init__(**kwargs)

        self.filePath = 'log.txt'
        self.dataLogging = False

        ## Schedules port-checking function
        self.schedule_get_ports()

        self.list_ports = get_serial_ports()

        for i in range(len(self.list_ports)):
            btn = Button(
                text=self.list_ports[i],
                size_hint_y=None,
                height=44)
            btn.bind(
                on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.ids.btn_dropdown.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=self.dropdown_callback)

    def dropdown_callback(self, instance, x):

        # Sets chosen port and sets text of main dropdown button.

        setattr(self.ids.btn_dropdown, 'text', x)
        self.chosen_port = x

    def switch_callback(self, instance, value):
        self.dataLogging = value

    def getFilePath(self, *args):
        try:
            saveFileDialog(self)
        except:
            pass

    def get_ports(self, dt):

        # Will update list of ports and, if new list is different from
        # old list, dismisses old dropdown menu and generates a new one.

        prev_list_ports = self.list_ports
        self.list_ports = get_serial_ports()

        ## If the new list is different from the old one, will update dropdown.
        if prev_list_ports != self.list_ports:

            ## Deletes current dropdown.
            self.ids.btn_dropdown.unbind(on_release=self.dropdown.open)
            self.dropdown.dismiss()

            ## Generates a new dropdown.
            self.dropdown = DropDown()

            for i in range(len(self.list_ports)):
                btn = Button(
                    text=self.list_ports[i],
                    size_hint_y=None,
                    height=44)
                btn.bind(
                    on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)

            self.ids.btn_dropdown.bind(on_release=self.dropdown.open)
            self.dropdown.bind(on_select=self.dropdown_callback)

    def start_reading(self):

        serial = start_serial(self)

        if serial != None:
            if self.change_timers():
                self.serial = serial
                self.manager.current = 'main'

    def change_timers(self):

        # If we could open the serial port, we
        # unschedule previous timer and
        try:
            self.unschedule_get_ports()
        except:
            self.serial.close()
            print("error unscheduling timer")
            return False

        # set timer to read port
        try:
            self.schedule_read_serial()
        except:
            self.serial.close()
            self.schedule_get_ports()
            print("error scheduling new timer")
            return False

        return True

    def schedule_get_ports(self):
        self.Timer_get_ports = Clock.schedule_interval(self.get_ports, 1)

    def unschedule_get_ports(self):
        self.Timer_get_ports.cancel()
        self.Timer_get_ports = None

    def schedule_read_serial(self):
        # If the frequency is changed, be sure to update the multiplier used
        # to send data to server too
        self.Timer_read_buffer = Clock.schedule_interval(
            lambda dt: read_serial(self.serial, dt, self.dataLogging), 0.02)

    def unschedule_read_serial(self):
        self.Timer_read_buffer.cancel()
        self.Timer_read_buffer = None

    pass

home_screen = HomeScreen(name='home')
