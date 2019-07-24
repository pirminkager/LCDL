
def read_data(mode,LCO):
    # Create a tuple of 4 voltage objects
    # Import Functionality of Analog Input Module
    from lucidIo.LucidControlAI4 import LucidControlAI4

    # Import Value Type for accessing voltages and currents
    from lucidIo.Values import ValueVOS4, ValueCUS4

    # Import LucidControl return values
    from lucidIo import IoReturn
    ai4 = LCO
    
    if mode == "C":
        values = (ValueCUS4(), ValueCUS4(), ValueCUS4(), ValueCUS4())
    elif mode == "V":
        values = (ValueVOS4(), ValueVOS4(), ValueVOS4(), ValueVOS4())
    else:
        exit()
    
    # Initialize a boolean tuple for channels to read.
    channels = (True, True, True, True)
    
    # Read the values of all voltage channels
    ret = ai4.getIoGroup(channels, values)

    if mode == "C":
        data = [values[0].getCurrent(), values[1].getCurrent(),
            values[2].getCurrent(), values[3].getCurrent()]
    elif mode == "V":
        data = [values[0].getVoltage(), values[1].getVoltage(),
            values[2].getVoltage(), values[3].getVoltage()]
    else:
        exit()

    if (ret == IoReturn.IoReturn.IO_RETURN_OK):
        status = 1
    else:
        status = 0
    
    return data,status



#### Test Section ####

if __name__ == '__main__':

    import serial_ports

    # Import Functionality of Analog Input Module
    from lucidIo.LucidControlAI4 import LucidControlAI4

    # Import Value Type for accessing voltages and currents
    from lucidIo.Values import ValueVOS4, ValueCUS4

    # Import LucidControl return values
    from lucidIo import IoReturn

    print ('START LOGGER')

    # Open AI4 port
    while True:
        try:

            print (serial_ports.serial_ports())

            comport = raw_input("Select Com Port: ")
            ai4 = LucidControlAI4(comport)


            
            if (ai4.open() == False):
                print ('Error connecting to port {0} '.format(
                    ai4.portName))
                ai4.close()
                exit()
	
            print ('PORT OPENED')

        except:
            continue
        break
    mode = 'C'
    stat,data = read_data(mode)
    print(data)
    if (stat == IoReturn.IoReturn.IO_RETURN_OK):
        print ('{0};mA;{1};mA;{2};mA;{3};mA'.format(
            data[0], data[1],
            data[2], data[3]))

    else:
        print ('Error reading CH0, CH1, CH2 and CH3 voltages')
        ai4.close()
        exit()

