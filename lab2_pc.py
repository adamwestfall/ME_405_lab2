import serialManager, time
from matplotlib import pyplot as p

#Plotting encoder position vs time
def plotResponse(out: list):
    pass

def initTestOne(s, ):
    s.writeToVCP()

if __name__ == '__main__':
    s = serialManager.SerialManager('COM3', 115200)
    k1 = 10
    k2 = 1000
    k3 = 42

    out_1 = initTest(s)
    out_2 = initTest(s)
    out_3 = initTest(s)

    plotResponse(out_1)
    plotResponse(out_2)
    plotResponse(out_3)