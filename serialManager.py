import serial as s


# Write a setpoint, read a position, write a setpoint...
# store each position and time
# plot the result at the end of the test
class SerialManager:
    
    def __init__(self, comport, baudrate):
        self.comport = comport
        self.baudrate = baudrate
        self.ready = 0
        self.busy = 1

    def getComport(self):
        return self.comport
    
    def getBaudrate(self):
        return self.baudrate
    
    # write to the serial to perform step responses with the controller
    # - writing a consistent setpoint for the controller
    def writeToVCP(self, line):
        with s.Serial(self.comport, self.baudrate) as s_port:
            # t = bytes(line)
            s_port.write(b"test")

    def readFromVCP(self):
        with s.Serial(self.comport,self.baudrate) as s_port:
            comOutput = s_port.read()

        return comOutput
    
