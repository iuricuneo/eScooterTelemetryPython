class DataSet:

    # Class that receives data and prints received data in one line of a file.

    # Upon creation, can receive a file name, otherwise default 'log.txt' Will
    # be used.

    # Will receive the following parameters:
    #     - solldrehzahl
    #     - lipo
    #     - batt
    #     - beschV
    #     - beschH
    #     - beschL
    #     - beschR
    #     - inc
    #     - state
    #     - accelState

    # After all data is received, will get the average value of input data and
    # write the averages in the file before cleaning the vectors for new
    # inputs.

    # Has 4 methods:
    #     - DataSet.init_file() will open the file and write keys to first line
    #     - DataSet.update() will check controls. If ready to save, will write
    #       data to the file and clear vectors
    #     - DataSet.clear() will clear vectors
    #     - DataSet.close() will close the file

    # To send using DataSet.update() it is necessary to set DataSet.control
    # values. It will receive the same parameters and one extra called
    # 'readyToSave'. If either all 7 other parameters are true, or
    # 'readyToSave' is true, will write the data.

    def __init__(self, _file = 'log.txt'):


        # Class constructor. DataSet has 4 attributes: data, control, File and
        # first_time_mark, that contains initial time mark.
        # Can receive one parameter, file name.
        # After opening file and initializing variables, will write to file
        # the keys of the DataSet.data dictionary.

        # Initializes class attributes

        # Inputs must be appended to data
        self.data = { 'solldrehzahl' : [0] ,
                      'batt' : [0] ,
                      'lipo' : [0] ,
                      'beschV' : [0] ,
                      'beschH' : [0] ,
                      'beschR' : [0] ,
                      'beschL' : [0] ,
                      'inc' : [0] ,
                      'state' : [0] ,
                      'accelState' : [0] ,
                      'time' : 0,
                      'sample' : 0 }

        # Control must have 'readyToSave' true, or all others true to write data
        self.control = { 'solldrehzahl' : False,
                         'batt' : False,
                         'lipo' : False,
                         'beschV' : False ,
                         'beschH' : False ,
                         'beschR' : False,
                         'beschL' : False,
                         'inc' : False,
                         'state' : False,
                         'accelState' : False,
                         'readyToSave' : False }

        # Will hold the pointer to the file.
        self.File = None

        self.first_time_mark = None


    def init_file(self, filePath):

        self.File = open(filePath, 'w')

        # Print to file the keys of DataSet.data
        lineToPrint = ''

        # Add keys to string
        for i in self.data.keys():
            lineToPrint += (i + ', ')

        # Take care of last comma and add line break
        lineToPrint = lineToPrint.rstrip(', ') + '\n'

        # Write to file
        self.File.write(lineToPrint)

        self.data['sample'] = 0

    def clear(self):

        # Clears dictionaries for new data. Can be called by user anytime, but
        # will be called by DataSet.update() after writing data to file.

        # Reset data
        for i in self.data.keys():
            if i != 'sample':
                self.data[i] = [0]

        # Reset control
        for i in self.control.keys():
            self.control[i] = False

    def update(self):

        from time import time

        # Updates the file with new data.
        # Will check controls and, if should write, then gets averages and
        # writes them to the file.

        # Auxiliar variable to check if all controls are true
        send = True

        # If 'readyToSave' is False, check other controls
        if not self.control['readyToSave']:
            # Will iterate through DataSet.control
            for i in self.control:
                # and, if current key isn't 'readyToSave',
                if i != 'readyToSave':
                    # will check if it is true.
                    send = send and self.control[i]

        # If all controls are true, or if 'readyToSave' is true, send is true
        self.control['readyToSave'] = send

        # So, if we are going to send,
        if self.control['readyToSave']:

            # We set local variables
            tmp = 0
            lineToPrint = ''

            # And iterate through the data
            for j in self.data.keys():
                if j == 'sample':
                    lineToPrint += (str(self.data[j]) + ', ')
                    self.data[j] += 1
                elif j == 'time':
                    # If we don't have a first time, get it
                    if self.first_time_mark is None:
                        self.first_time_mark = time()
                    # Get current time and save it
                    self.data[j] = (time() - self.first_time_mark) * 1000
                    lineToPrint += (str(self.data[j]) + ', ')
                elif j != 'sample':
                    # For every data key, we will add all inputs to tmp
                    for k in self.data[j][1:]:
                        tmp += k
                    # and try to get average.
                    try:
                        self.data[j][0] = tmp/(len(self.data[j])-1)
                    except:
                        # If can't get average, no value was entered. (err = n/0)
                        self.data[j][0] = 0
                    # Then, add value to line
                    lineToPrint += (str(self.data[j][0]) + ', ')
                    # and reset tmp.
                    tmp = 0

            # Deal with last comma and add line break
            lineToPrint = lineToPrint.rstrip(', ') + '\n'

            # Write to file
            self.File.write(lineToPrint)

            # Clear dictionaries
            self.clear()

        # Then, return send. Will be true if sent, false if didn't send.
        return send

    def close(self):

        # Clears memory before closing file to save it.

        self.clear()
        self.File.close()
