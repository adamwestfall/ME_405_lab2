import serialManager, time
from matplotlib import pyplot as p


def listen(s):
    print("Listening to uart...",end='')
    test = s.readFromVCP()
    if len(test) == 0:
        print("I listened and heard nothing")

    else:
        print("This is what I heard:")
        for line in test:
            print(line)


if __name__ == '__main__':
    # Constants
    BAUDRATE = 115200
    COMPORT = 4

    print("Initializing serial manager...", end = "")
    s = serialManager.SerialManager('COM'+str(COMPORT), BAUDRATE)
    print("done")
    # line1 = bytes('test')
    print("Starting test...")
    try:

        while (True):
            listen(s)
            line1 = input("Enter some text: ")
            # line1 = "!" + pref
            # print(line1.encode())
            s.writeToVCP(line1)
            print("done")
            # line2 = s.readFromVCP()
            # print("Contents of the VCP: " + str(line2))
    except EOFError:
        print('Closing serial port')
        # s.close()

    except KeyboardInterrupt:
        print('Closing serial port')
        # s.close()