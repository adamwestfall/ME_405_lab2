'''   @file                            lab2_pc.py
   @brief                              Plots closed loop controller response.
   @details                            Plots closed loop controller response. Utilizes the plotResponse and initTest functions.                                       
   @author                             Jason Davis
   @author                             Conor Fraser
   @author                             Adam Westfall
   @copyright                          Creative Commons CC BY: Please visit https://creativecommons.org/licenses/by/4.0/ to learn more
   @date                               January 9, 2023
'''

import serialManager, time
from matplotlib import pyplot as p

#Plotting encoder position vs time
def plotResponse(results: list, gain, target_pos, test_num):
    '''!  @brief                              Plots the response of the test results.
       @details                               Plots the response of the test results. Sets x and y axis labels.
                                              Sets the title of the plot. The x and y data start as empty lists and
                                              get appended as data is collected.
       @param list                            Parses in a list of parameters to hit the low Kp, high Kp, and best performance targets.
       @param gain                            Parses in the Kp.    
       @param target_pos                      Parses in the target motor position.
       @param test_num                        Parses in which test is running.
    '''
    p.title("Test %s: Theta vs Time"%(str(test_num)))
    p.xlabel("Time, seconds")
    p.ylabel("Theta, encoder_ticks")
    p.grid(True)

    offsetFound = False
    offset = 0
    x = []
    y = []

    for line in results:
        i = line.strip('!').split(',')
        if not offsetFound:
            offset = int(i[0])
            offsetFound = True
        x.append(int(i[0])/offset)
        y.append(int(i[1]))
    p.plot(x,y)
    p.show()


def initTest(s, k, pos, testNum):
    '''!  @brief                              Initial test of the controller.
       @details                               Conducts the initial controller test.
       @param s                               Parses in the serial manager object.
       @param k                               Parses in the Kp for testing.    
       @param pos                             Parses in the target motor position.
       @param testNum                         Parses in which test is running.
       @return                                Returns the results of the test.
    '''
    line = str(k) + "," + str(pos)

    print("Sending test parameters over " + str(s.getComport()) + "...",end='')
    s.writeToVCP(line)
    print("done")
    print("Ready to receive test results: ")

    results = s.readFromVCP()
    print("***************** Test " + str(testNum) + " Complete ****************")
    return results

if __name__ == '__main__':
    # Constants
    BAUDRATE = 115200
    COMPORT = 4

    print("Initializing serial manager...", end = "")
    s = serialManager.SerialManager('COM' + str(COMPORT), BAUDRATE)
    print("done")
    
    try:
        #   Sample of data sent to VCP
        #   "10,2000\n\r"
        k1 = 3
        k2 = 100
        k3 = 50
        target_pos = 8000
        # target_pos2 = 8000

        # Starts in write mode, changes over to read mode
        out_1 = initTest(s, k1, target_pos, 1)
        time.sleep(1)
        out_2 = initTest(s, k2, target_pos, 2)
        time.sleep(1)
        out_3 = initTest(s, k3, target_pos, 3)
        print("Controller tests complete")

        plotResponse(out_1, k1, target_pos, 1)
        plotResponse(out_2, k2, target_pos, 2)
        plotResponse(out_3, k3, target_pos, 3)

    except KeyboardInterrupt:
        print("Program terminated")

