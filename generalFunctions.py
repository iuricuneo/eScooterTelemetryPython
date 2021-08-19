def get_serial_ports():

    # Will scan windows's serial ports and look for available ports.
    # Returns a list with the available ports.

    import serial

    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except:
            pass
    return result

def prepare_screen_change(MS, HS):

    # Function to return from mainScreen to homeScreen

    from kivy.clock import Clock

    if HS.dataLogging and not MS.ds.File.closed:
        MS.ds.close()

    if HS.serial.isOpen():
        #HS.serial.cancel_read()  -> shouldn't be needed
        HS.serial.close()

    MS.reset_plots()

    HS.unschedule_read_serial()

    HS.schedule_get_ports()

def saveFileDialog(HS):

    # Open a Windows File 'Save' Dialog.
    # The function is asynchronous, so the successful callback will change
    # the attribute from the main screen directly. However, the script will
    # return to main screen code.

    from kivy.uix.popup import Popup
    from functools import partial
    from os.path import sep, expanduser, isdir, dirname
    from os import getcwd
    import sys
    import getpass

    from components.filebrowser import FileBrowser

    # Get path to desktop and check if it exists. If it doesn't, just show
    # current directory.
    # The screen must be shown in a popup, which must be closed afterwards.

    _path = dirname(expanduser('~')) + sep + getpass.getuser() + sep + 'Desktop'

    def fbrowser_canceled(popup, instance):
        popup.dismiss()

    def fbrowser_success(popup, instance):

        if instance.filename != '':
            filename = instance.filename
        else:
            filename = instance.selection[0]

            # If user selected a file that already exists, gets only the
            # file name and path to overwrite
        if filename[1] == ':' or filename.startswith((sep + sep)):
            parts = filename.split(sep)
            file_path = ''
            try:
                for i in parts[0:-1]:
                    file_path += i + sep
            except BaseException as e:
                print('Failed to get path: ' + str(e))
            filename = parts[-1]
        else:
            file_path = instance.path + sep

        size_filename = len(filename.split('.'))

        # If user chose no extension, adds '.txt'
        if size_filename == 1:
            filename += '.txt'
        elif size_filename < 1:
            return

        HS.filePath = (file_path + filename).replace('\\','/')

        popup.dismiss()

    if isdir(_path):
        browser = FileBrowser(select_string='Save', path=_path,
                              selection=['log.txt'], filters=['*.txt','*.log'])

    else:
        browser = FileBrowser(select_string='Save', path=getcwd(),
                              selection=['log.txt'], filters=['*.txt','*.log'])

    popup = Popup(title="Save", content=browser,
                  size_hint=(0.9, 0.9), auto_dismiss=False)

    browser.bind( on_success=partial(fbrowser_success, popup),
                  on_canceled=partial(fbrowser_canceled, popup) )

    popup.open()

    '''
    import win32ui, win32con

    #openFlags = win32con.OFN_OVERWRITEPROMPT|win32con.OFN_FILEMUSTEXIST

    dlg = win32ui.CreateFileDialog(0, 'txt', 'log')

    if dlg.DoModal()!=win32con.IDOK:
        dlg.__del__()
        return None

    path = dlg.GetPathNames()[0]

    del(dlg)

    return path
    '''


def start_serial(HS):

    # Called when user presses button 'naechste', will interpret entered
    # data and get a serial port with it.
    # Returns None if couldn't get port for any reason, else returns the  port.

    import serial
    from screens.mainScreen import main_screen

    ser = None

    try:
        br = int(HS.ids.baudrate.text)
        index = HS.list_ports.index(HS.chosen_port)
    except:
        return None

    if HS.chosen_port != '' and br > 0 and index >= 0:
            # If a port was chosen,
        try:

            ## Get entered data
            Port = HS.chosen_port
            Baudrate = HS.chosen_baudrate = br
            Stopbits = HS.chosen_stopbits = int(HS.ids.stopbits.text)
            Bytesize = HS.chosen_bytesize = int(HS.ids.bytesize.text)
            Timeout = HS.chosen_timeout = float(HS.ids.timeout.text)

            _parity = HS.ids.parity.text.strip().upper().replace(" ","")
            _rtscts = HS.ids.rtscts.text.strip().upper().replace(" ","")

            ## Interprets entered data.

            if Timeout <= 0:
                return None

            if _parity.startswith('PARITY'):
                _parity = _parity[6:]

            if _parity.startswith('N'):
                Parity = serial.PARITY_NONE
            elif _parity.startswith('O'):
                Parity = serial.PARITY_ODD
            elif _parity.startswith('E'):
                Parity = serial.PARITY_EVEN
            elif _parity.startswith('M'):
                Parity = serial.PARITY_MARK
            elif _parity.startswith('S'):
                Parity = serial.PARITY_SPACE
            else:
                return None

            if ( _rtscts.startswith('RTS') or _rtscts.startswith('CTS') or
                 _rtscts.startswith('AN') or _rtscts.startswith('ON') or
                 _rtscts.startswith('1') or _rtscts.startswith('T') or
                 _rtscts.startswith('Y') or _rtscts.startswith('J') or
                 _rtscts.startswith('W') ):
                Rtscts = HS.chosen_rtscts = 1
            elif ( _rtscts.startswith('AU') or _rtscts.startswith('OF') or
                   _rtscts.startswith('0') or _rtscts.startswith('F') or
                   _rtscts.startswith('N') or _rtscts.startswith('L') ):
               Rtscts = HS.chosen_rtscts = 0
            else:
                return None

            if Stopbits == 1:
                Stopbits = serial.STOPBITS_ONE
            elif Stopbits == 1.5:
                Stopbits = serial.STOPBITS_ONEPOINT_FIVE
            elif Stopbits == 2:
                Stopbits = serial.STOPBITS_TWO
            else:
                return None

            if Bytesize == 5:
                Bytesize = serial.FIVEBITS
            elif Bytesize == 6:
                Bytesize = serial.SIXBITS
            elif Bytesize == 7:
                Bytesize = serial.SEVENBITS
            elif Bytesize == 8:
                Bytesize = serial.EIGHTBITS
            else:
                return None

            # opens serial port

            ser = serial.Serial(
                port=Port,
                baudrate=Baudrate,
                parity=Parity,
                stopbits=Stopbits,
                bytesize=Bytesize,
                timeout=Timeout,
                xonxoff=0,
                rtscts=Rtscts)

            # starts data-logging if selected

            if HS.dataLogging:
                main_screen.ds.init_file(HS.filePath)

        except:
            return None

    return ser

def read_serial(ser, dt, dataLogging=False):

    # Will read buffer from chosen xbee module.

    import serial
    from screens.mainScreen import main_screen
    from screens.settingsScreen import settings_screen

    buffer_data = ""

    # If we read alright, counter will be reset anyway
    if main_screen.signalImgCounter < main_screen.numMsgToNoSignal:
        main_screen.signalImgCounter += 1

    try:

        # Will read buffer until there is nothing left.
        # This ensures that packages with only 1 byte won't affect us.

        while ser.inWaiting() != 0:

            ## Reads 2 bytes of data
            buffer_data = ser.read(3)

            try:

                ## If we got 2 bytes, strip id and data.
                if len(buffer_data) == 3:
                    _id = buffer_data[0]
                    data1 = buffer_data[1]
                    data2 = buffer_data[2]

                    if main_screen.settings['dataToServer']:

                        main_screen.counterToUpdateServer += 1
                        # If interval changes, the value 0.02 must match the
                        # new interval value
                        if (main_screen.counterToUpdateServer
                                >= (main_screen.settings['timeToSend'] / 0.02)):

                            main_screen.counterToUpdateServer = 0

                            import requests
                            import json

                            url = 'http://thiproject-carapp.herokuapp.com/data'

                            payload = main_screen.dataToServer

                            for i in payload.keys():
                                payload[i] = str(payload[i])

                            headers = {
                                "content-type": "application/json",
                                "Authorization": "<auth-key>"
                            }

                            r = requests.put( url,
                                              data=json.dumps(payload),
                                              headers=headers )
                            print('data sent')

                else:
                    _id = 0

                # If we got a correct reading, reset counter
                if ( ( _id == ord('G') or _id == ord('V') or
                       _id == ord('B') or _id == ord('I') )
                   and main_screen.signalImgCounter > 0 ):
                        main_screen.signalImgCounter = 0

                ## Interprets message received
                if _id == ord('G'):

                    new_speed = int(data1/0.06)
                    main_screen.speed = str(new_speed)
                    new_lipo = data2/10
                    main_screen.lipo = str(new_lipo)

                    if main_screen.settings['lipoColor'] and new_lipo < 14:
                        main_screen.ids.lipolayout.col = (250/255,
                                                          100/255,
                                                          100/255)
                    else:
                        main_screen.ids.lipolayout.col = (200/255,
                                                          200/255,
                                                          200/255)

                    if dataLogging:
                        main_screen.ds.data['solldrehzahl'].append(new_speed)
                        main_screen.ds.data['lipo'].append(new_lipo)
                        main_screen.ds.control['solldrehzahl'] = True
                        main_screen.ds.control['lipo'] = True

                    main_screen.update_plot()

                    if main_screen.settings['dataToServer']:
                        main_screen.dataToServer['speed'] = new_speed
                        main_screen.dataToServer['lipo'] = new_lipo

                elif _id == ord('B'):

                    new_batt = ( (data1 << 8) + data2 ) / 10
                    main_screen.batt = str(new_batt)

                    if main_screen.settings['battColor'] and new_batt < 33:
                        main_screen.ids.mainbattlayout.col = (250/255,
                                                              100/255,
                                                              100/255)
                    else:
                        main_screen.ids.mainbattlayout.col = (200/255,
                                                              200/255,
                                                              200/255)

                    if dataLogging:
                        main_screen.ds.data['batt'].append(new_batt)
                        main_screen.ds.control['batt'] = True

                    if main_screen.settings['dataToServer']:
                        main_screen.dataToServer['batt'] = new_batt

                elif _id == ord('I'):
                    new_inclination = ( (data1 << 8) + data2 ) / 10
                    main_screen.inclination = int(new_inclination)
                    if dataLogging:
                        main_screen.ds.data['inc'].append(new_inclination)
                        main_screen.ds.control['inc'] = True

                    if main_screen.settings['dataToServer']:
                        main_screen.dataToServer['inclination'] = new_inclination

                elif _id == ord('S'):

                    '''

                    data1 contains accelState
                    data2 is made up of: 0000_0000
                                  state <-'  |  '-> mode
                    '''


                    new_mode = data2 & 0x0f

                    if new_mode == 2:
                        main_screen.mode = './img/security_icon.png'
                    elif new_mode == 1:
                        main_screen.mode = './img/forward_icon.png'
                    else:
                        main_screen.mode = './img/transparency.png'

                    new_state = data2 >> 4

                    if main_screen.settings['stateImg']:

                        if new_state == 8:
                            main_screen.state = './img/no_batt.png'
                        elif new_state == 1 or new_state == 2:
                            main_screen.state = './img/setup.png'
                        else:
                            main_screen.state = './img/transparency.png'

                    else:
                        main_screen.state = './img/transparency.png'

                    new_accel_state = data1

                    if main_screen.settings['speedColor']:

                        if new_accel_state == 0:
                            main_screen.accel_state = '#c8c8c8' #keep
                        elif new_accel_state == 1:
                            main_screen.accel_state = '#a7c8a8' #accel
                        else:
                            main_screen.accel_state = '#c8a7a7' #decel
                    else:
                        main_screen.accel_state = '#c8c8c8'

                    if dataLogging:
                        main_screen.ds.data['state'].append(new_state)
                        main_screen.ds.data['accelState'].append(new_accel_state)
                        main_screen.ds.control['state'] = True
                        main_screen.ds.control['accelState'] = True

                    if main_screen.settings['dataToServer']:
                        main_screen.dataToServer['mode'] = new_mode
                        main_screen.dataToServer['state'] = new_state
                        main_screen.dataToServer['accelState'] = new_accel_state

                # Firmwares version 1.0 don't use acceleration sensor data.
                elif _id == ord('V'):

                    if main_screen.settings['dataToServer']:
                        main_screen.dataToServer['accel'] = data1
                        main_screen.dataToServer['inc'] = data2

                    # only change color if set to
                    if main_screen.settings['incColor'] and (
                        main_screen.left_arrow == './img/red-left.png' or
                        main_screen.right_arrow == './img/red-right.png' ):

                        main_screen.ids.accellayout.col = (250/255,
                                                           100/255,
                                                           100/255)
                        main_screen.ids.accelbutton.background_color = (250/255,
                                                                        100/255,
                                                                        100/255,
                                                                        1)

                    else:

                        main_screen.ids.accellayout.col = (200/255,
                                                           200/255,
                                                           200/255)
                        main_screen.ids.accelbutton.background_color = (200/255,
                                                                        200/255,
                                                                        200/255,
                                                                        1)

                    if data1 == 0:
                        main_screen.up_arrow = './img/white-up.png'
                        main_screen.down_arrow = './img/white-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(0)
                            main_screen.ds.data['beschH'].append(0)
                    elif data1 == 1:
                        main_screen.up_arrow = './img/green-up.png'
                        main_screen.down_arrow = './img/white-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(1)
                            main_screen.ds.data['beschH'].append(0)
                    elif data1 == 2:
                        main_screen.up_arrow = './img/orange-up.png'
                        main_screen.down_arrow = './img/white-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(2)
                            main_screen.ds.data['beschH'].append(0)
                    elif data1 == 3:
                        main_screen.up_arrow = './img/red-up.png'
                        main_screen.down_arrow = './img/white-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(3)
                            main_screen.ds.data['beschH'].append(0)
                    elif data1 == 4:
                        main_screen.up_arrow = './img/white-up.png'
                        main_screen.down_arrow = './img/green-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(0)
                            main_screen.ds.data['beschH'].append(1)
                    elif data1 == 5:
                        main_screen.up_arrow = './img/white-up.png'
                        main_screen.down_arrow = './img/orange-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(0)
                            main_screen.ds.data['beschH'].append(2)
                    else:
                        main_screen.up_arrow = './img/white-up.png'
                        main_screen.down_arrow = './img/red-down.png'
                        if dataLogging:
                            main_screen.ds.data['beschV'].append(0)
                            main_screen.ds.data['beschH'].append(3)

                    if data2 == 0:
                        main_screen.right_arrow = './img/white-right.png'
                        main_screen.left_arrow = './img/white-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(0)
                            main_screen.ds.data['beschR'].append(0)
                    elif data2 == 1:
                        main_screen.right_arrow = './img/green-right.png'
                        main_screen.left_arrow = './img/white-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(0)
                            main_screen.ds.data['beschR'].append(1)
                    elif data2 == 2:
                        main_screen.right_arrow = './img/orange-right.png'
                        main_screen.left_arrow = './img/white-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(0)
                            main_screen.ds.data['beschR'].append(2)
                    elif data2 == 3:
                        main_screen.right_arrow = './img/red-right.png'
                        main_screen.left_arrow = './img/white-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(0)
                            main_screen.ds.data['beschR'].append(3)
                    elif data2 == 4:
                        main_screen.right_arrow = './img/white-right.png'
                        main_screen.left_arrow = './img/green-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(1)
                            main_screen.ds.data['beschR'].append(0)
                    elif data2 == 5:
                        main_screen.right_arrow = './img/white-right.png'
                        main_screen.left_arrow = './img/orange-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(2)
                            main_screen.ds.data['beschR'].append(0)
                    else:
                        main_screen.right_arrow = './img/white-right.png'
                        main_screen.left_arrow = './img/red-left.png'
                        if dataLogging:
                            main_screen.ds.data['beschL'].append(3)
                            main_screen.ds.data['beschR'].append(0)

                    main_screen.ds.control['beschV'] = True
                    main_screen.ds.control['beschH'] = True
                    main_screen.ds.control['beschL'] = True
                    main_screen.ds.control['beschR'] = True

            except Exception as e:
                print(e)
                return

            if dataLogging:
                # These commented lines are to be used in case
                # only some of the variables are of interest.
                #ctr = main_screen.ds.control
                #if ctr['batt']:
                #    ctr['readyToSave'] = True

                main_screen.ds.update()

    ## If error here such as no port found, returns to HomeScreen.
    except serial.SerialException as e:
        # This exception is probably raised by stop_reading() itself, so just
        # return.
        return
    except:
        main_screen.stop_reading()
        return
