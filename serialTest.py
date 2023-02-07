import serialManager, time
from matplotlib import pyplot as p

if __name__ == '__main__':
    s = serialManager.SerialManager('COM4', 115200)
    line1 = bytes('test')
    s.writeToVCP(line1)
    line2 = s.readFromVCP()
    print("Contents of the VCP: " + str(line2))