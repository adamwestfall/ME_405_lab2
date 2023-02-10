'''   @file                            serialManager.py
   @brief                              Initializes and communicates with Virtual Comport(VCP).
   @details                            Contains a SerialManger class with an init, getComport, getBaudrate, writeToVCP, and readFromVCP functions.                                     
   @author                             Jason Davis
   @author                             Conor Fraser
   @author                             Adam Westfall
   @copyright                          Creative Commons CC BY: Please visit https://creativecommons.org/licenses/by/4.0/ to learn more
   @date                               January 9, 2023
'''

import serial


# Write a setpoint, read a position, write a setpoint...
# store each position and time
# plot the result at the end of the test
class SerialManager:
    '''!  @brief                              Serial Manager class.
       @details                               Contains init, getComport, getBaudrate, writeToVCP, and readFromVCP functions. 
    '''
    
    def __init__(self, COMPORT, BAUDRATE):
        '''!  @brief                              Initializes the serial port with comport and baudrate values.
           @details                               Initializes the serial port with comport and baudrate values that are parsed in as parameters.
           @param COMPORT                         Parses in the COMPORT for the serial port.
           @param BAUDRATE                        Parses in the BAUDRATE for the serial port.            
        '''
        self.COMPORT = COMPORT
        self.BAUDRATE = BAUDRATE
        self.serial_port = serial.Serial(port = self.COMPORT, baudrate = self.BAUDRATE, stopbits = 1, timeout = 3)

    def getComport(self):
        '''!  @brief                              Returns the COMPORT value.
           @details                               Returns the COMPORT value.
           @return                                Returns the COMPORT value.
        '''
        return self.COMPORT
    
    def getBaudrate(self):
        '''!  @brief                              Returns the BAUDRATE value.
           @details                               Returns the BAUDRATE value.
           @return                                Returns the BAUDRATE value.
        '''
        return self.BAUDRATE
    
    # write to the serial to perform step responses with the controller
    # - writing a consistent setpoint for the controller
    def writeToVCP(self, line):
        '''!  @brief                              Writes serial data to the VCP.
           @details                               Utilizes the "with" and "as" commands to interact with the serial port.
                                                  Encodes data to be sent by serial communication.
           @param line                            Parses in a line of data to encode.
        '''
        with self.serial_port as s_port:
            s_out = line.encode()
            s_port.write(s_out)
            s_port.flush()
        s_port.close()

    # We're getting memory allocation errors. We need to do this more efficiently!
    def readFromVCP(self):
        '''!  @brief                              Reads serial data from the VCP.
           @details                               Utilizes the "with" and "as" commands to interact with the serial port.
                                                  Decodes the data coming form the VCP.
           @return                                Returns the comOutput as a list filled with decoded line data.
        '''
        comOutput = []
        line = ""

        with self.serial_port as s_port:
            charIn = s_port.read().decode()
            while charIn != '':
                line = line + charIn
                # print(str(s_port.in_waiting) + " bytes in waiting")
                # print("charIn: " + str(charIn))
                if charIn == '!':
                    comOutput.append(line)
                    line = ""
                charIn = s_port.read().decode()

            s_port.flush()
        s_port.close()

        return comOutput