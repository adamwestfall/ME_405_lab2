import serialManager, time
from matplotlib import pyplot as p

if __name__ == '__main__':
    print("Initializing serial manager...")
    s = serialManager.SerialManager('COM4', 115200)
    print("done.")
    # line1 = bytes('test')
    print("Starting test...")
    line1 = 'test\r'
    s.writeToVCP(line1)
    print("done")
    line2 = s.readFromVCP()
    print("Contents of the VCP: " + str(line2))