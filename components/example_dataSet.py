from dataSet import DataSet

# Initiates with file name (default = 'log.txt')
ds = DataSet('data.txt')

# Enters data
ds.data['lipo'].append(14.8)
ds.data['lipo'].append(14.6)

# Sets control to true
ds.control['lipo'] = True

# Enters more data
ds.data['solldrehzahl'].append(3000)
ds.data['solldrehzahl'].append(2000)
ds.data['solldrehzahl'].append(1000)
ds.data['solldrehzahl'].append(0)

# Sets control to true
ds.control['solldrehzahl'] = True

# Enters more data
ds.data['batt'].append(36)
ds.data['batt'].append(34)

# Sets control to true
ds.control['batt'] = True

# Enters more data
ds.data['beschV'].append(1)
ds.data['beschV'].append(2)

# Sets control to true
ds.control['beschV'] = True

# Sets control to true so that data can be sent, beschH will be 0.
ds.control['beschH'] = True

# Writes to file and, if successful, reset vectors. Else, just reset
True if ds.update() else ds.clear()

# Now, both dictionaries were cleared. If DataSet.update() is called, nothing
# will happen, because controls are false.
ds.update()

# Enters all data
ds.data['lipo'].append(14.8)
ds.data['lipo'].append(14.6)

ds.data['solldrehzahl'].append(3000)
ds.data['solldrehzahl'].append(2000)
ds.data['solldrehzahl'].append(1000)
ds.data['solldrehzahl'].append(0)

ds.data['batt'].append(36)
ds.data['batt'].append(34)

ds.data['beschV'].append(1)
ds.data['beschV'].append(2)

ds.data['beschH'].append(3)
ds.data['beschH'].append(3)
ds.data['beschH'].append(3)
ds.data['beschH'].append(3)
ds.data['beschH'].append(3)
ds.data['beschH'].append(3)
ds.data['beschH'].append(3)

# Sets controls to true ('readyToSave' can be set as well, but no need)
for i in ds.control.keys():
    if i != 'readyToSave':
        ds.control[i] = True

# Writes data and resets, or just reset
True if ds.update() else ds.clear()

# Enters data again
ds.data['lipo'].append(15.8)
ds.data['lipo'].append(14.6)

ds.data['solldrehzahl'].append(3000)
ds.data['solldrehzahl'].append(2000)
ds.data['solldrehzahl'].append(2751)
ds.data['solldrehzahl'].append(1200)
ds.data['solldrehzahl'].append(1000)
ds.data['solldrehzahl'].append(50)
ds.data['solldrehzahl'].append(0)

ds.data['batt'].append(36)
ds.data['batt'].append(34)

ds.data['beschV'].append(1)
ds.data['beschV'].append(2)

ds.data['beschH'].append(3)
ds.data['beschH'].append(2)
ds.data['beschH'].append(1)
ds.data['beschH'].append(0)
ds.data['beschH'].append(1)
ds.data['beschH'].append(2)
ds.data['beschH'].append(3)

# Sets control to true so we can write to file
ds.control['readyToSave'] = True

# Write to file and clear vectors, or just clear
True if ds.update() else ds.clear()

# Closes file
ds.close()
