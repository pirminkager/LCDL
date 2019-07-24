'''
Created on 11.07.2019

@author: Pirmin Kager
'''

import serial_ports
import read_data
import datetime
import time

# Import Functionality of Analog Input Module
from lucidIo.LucidControlAI4 import LucidControlAI4

# Import Value Type for accessing voltages and currents
from lucidIo.Values import ValueVOS4, ValueCUS4

# Import LucidControl return values
from lucidIo import IoReturn

if __name__ == '__main__':
    try:
        print ('START LOGGER\n')

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

                print("\nSelect mode:\n\n'V' .. 0-10V\n'C' .. 0-20ma\n")
                mode = raw_input("Enter Mode: ")
                print('')
                interval = input("Logging interval in seconds: ")
                filename = raw_input("\nEnter the filename: ")
                print ('\nPORT OPENED')

                print ('\n=========================================================================')
                print (' IDENTIFY DEVICE')
                print ('=========================================================================\n')
            
                ret = ai4.identify(0)
            
                if ret == IoReturn.IoReturn.IO_RETURN_OK:
                        print ('Device Class:       {0}'.format(ai4.getDeviceClassName()))
                        print ('Device Type:        {0}'.format(ai4.getDeviceTypeName()))
                        print ('Serial No.:         {0}'.format(ai4.getDeviceSnr()))
                        print ('Firmware Rev.:      {0}'.format(ai4.getRevisionFw()))
                        print ('Hardware Rev.:      {0}'.format(ai4.getRevisionHw()))
                else:
                        print ('Identify Error')
                        ai4.close()
                        exit()

                print('\n\nLogging to '+filename+'.csv')

            except:
                print('')
                continue
            break

        # Check if the module supports Current Value Type

        print('\n')
        
        supCurrent = False
        if (ai4.getDeviceTypeName() == "0 A ~ 0.02 A"):
            supCurrent = True

        while True:
            
            file = open(filename+'.csv', 'a')
            data,status=read_data.read_data(mode,ai4)
            ts = datetime.datetime.now()
            date = ts.strftime("%d-%m-%Y %H:%M:%S")
            
            if status == 1:

                line = date + ";" + str(data[0]) + ";" + str(data[1]) + ";" + str(data[2]) + ";" + str(data[3]) + ";\n"
                file.write(line.replace('.',','))
                file.close
                print(line[:-2])
                time.sleep(interval)
            else:
                time.sleep(0.01)
            
    except KeyboardInterrupt:
        print ('\nLogging Stopped')
        ai4.close()
        exit()
