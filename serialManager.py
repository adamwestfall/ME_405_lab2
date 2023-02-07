'''   @file                            serialManager.py
   @brief                              Serial Manager for the Motors and Controller.
   @details                            Instantiates a Serial Manager class with an init, getComport, getBaudrate,
                                       writeToVCP, and readFromVCP. The getComport and getBaudrate return their respective variables.
                                       The write and read to VCP function write and read data to the Virtual Comport.
   @author                             Jason Davis
   @author                             Conor Fraser
   @author                             Adam Westfall
   @copyright                          Creative Commons CC BY: Please visit https://creativecommons.org/licenses/by/4.0/ to learn more
   @date                               February 5, 2023
'''

import serial as s


# Write a setpoint, read a position, write a setpoint...
# store each position and time
# plot the result at the end of the test
class SerialManager:
    '''!   @brief      Establishes a Serial Manager Class.
       @details    Instantiates a Serial Manager class with an init, getComport, getBaudrate, writeToVCP, and readFromVCP.
    '''
    
    def __init__(self, comport, baudrate):
        '''!   @brief                   Instantiates our Serial Manager object.
           @details                     Instantiates comport, baudrate, ready, and busy variables.
           @param comport               Parses in the comport.
           @param baudrate              Parses in the baudrate.
        '''
        self.comport = comport
        self.baudrate = baudrate
        self.ready = 0
        self.busy = 1

    def getComport(self):
        '''!   @brief                   Returns the comport variable.
           @details                     Returns the comport variable.
           @return                      Returns the comport variable.
        '''
        return self.comport
    
    def getBaudrate(self):
        '''!   @brief                   Returns the baudrate variable.
           @details                     Returns the baudrate variable.
           @return                      Returns the baudrate variable.
        '''
        return self.baudrate
    
    # write to the serial to perform step responses with the controller
    # - writing a consistent setpoint for the controller
    def writeToVCP(self, line):
        '''!   @brief                   Writes serial data to the VCP.
           @details                     Uses a serial object, the comport variable, and the baudrate variable to write data.
           @param line                  COME BACK TO THIS, IS THIS NEEDED?
        '''
        with s.Serial(self.comport, self.baudrate) as s_port:
            # t = bytes(line)
            s_port.write(b"test")

    def readFromVCP(self):
        '''!   @brief                   Reads from the VCP.
           @details                     Reads the VCP data and returns that data as a comOutput variable.
           @return                      Returns the data read from the VCP as a comOutput variable.
        '''
        with s.Serial(self.comport,self.baudrate) as s_port:
            comOutput = s_port.read()

        return comOutput
    
