'''   @file                            main.py
   @brief                              Main function to run a closed loop motor controller.
   @details                            Requires the motor_driver, encoder, closed_loop_controller, serialManager, and lab2_pc files 
                                       to properly apply closed loop control on DC motors. This file contains writeTo, readFrom, initializeUART
                                       initializeHardware, and runControllerTest functions.                                       
   @author                             Jason Davis
   @author                             Conor Fraser
   @author                             Adam Westfall
   @copyright                          Creative Commons CC BY: Please visit https://creativecommons.org/licenses/by/4.0/ to learn more
   @date                               January 9, 2023
'''

import pyb, motor_driver, encoder, closed_loop_controller, utime
import numpy as np

def writeTo(external, test_results):
    '''!  @brief                              WriteTo function for writing test results.
       @details                               WriteTo function for writing test results. Used in testing.
       @param external                        External serial connection.
       @param test_results                    Parses in test results.      
    '''
    pass

def readFrom(external):
    '''!  @brief                              Read data from serial connection.
       @details                               Read data from serial connection.
       @param external                        External serial connection.
    '''
    pass
    test_data = external.read().decode()
    line = test_data.split(',')
    print("Gain: %s\t\tSetpoint: %s"%(line[0], line[1]))

    return int(line[0]), int(line[1])

def initializeUART():
    '''!  @brief                              Initializes UART.
       @details                               Initializes UART connection. BAUDRATE is set to 115200.
       @return                                Returns the initialized UART object.
    '''
    print("Initializing UART...",end='')
    BAUDRATE = 115200
    external_device = pyb.UART(2, baudrate=BAUDRATE)
    external_device.init(BAUDRATE, bits=8, parity=None, stop=1, read_buf_len=0)
    print('done')
    return external_device

def initializeHardware():
    '''!  @brief                              Initializes the motor, encoder, and closed loop controller.
       @details                               Motor, encoder, and controller objects are created. 
       @return                                Returns a list of the necessary hardware objects.
    '''
    print("Initializing hardware...",end='')
    # enable any motor and encoder pins, probaby imported
    enable1 = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    input1 = pyb.Pin.cpu.B4
    input2 = pyb.Pin.cpu.B5
    timer1 = pyb.Timer(3, freq=20000)

    # Creating motor 1 objects
    motor_1_driver = motor_driver.MotorDriver(enable1, input1, input2, timer1)
    print("motor_1_driver...",end='')
    motor_1 = motor_1_driver.motor(input1, input2, 1, 2, "MOTOR A")
    print("motor_1...",end='')

    # Creating encoder object for motor 1
    encoder_A = encoder.Encoder(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4, ID="ENCODER A")
    print("encoder_A...",end='')

    # Creating controller object
    controller1 = closed_loop_controller.Closed_loop_controller()
    print("controller_1...",end='')
    print("done")
    return [encoder_A, motor_1_driver, motor_1, controller1]

def runControllerTest(gain, setpoint, enc, driver, motor, controller, testNum):
    '''!  @brief                              Tests the controller.
       @details                               Tests the controller based on the Kp gain inputs from the user.
                                              Utilizes a while loop to constantly update the data. 
       @param gain                            Parses in the input gain.
       @param setpoint                        Parses in the angle setpoint for where we want the motor to stop.
       @param enc                             Parses in the encoder object.
       @param driver                          Parses in the motor_driver object.
       @param motor                           Parses in the motor object.
       @param controller                      Parses in the closed loop controller object.
       @param testNum                         Parses in the Test Counter.
       @return                                Returns a list of the necessary hardware objects.
    '''
    print("Running controller test " + str(testNum) + "...",end='')
    runtime = 10  # time in seconds
    step = 0.01  # time in seconds
    size = runtime / step

    results = np.zeros((int(size), 2))

    # Starting controller tests
    controller.set_kp(gain)
    controller.set_setpoint(setpoint)

    offset = utime.ticks_ms()
    current_time = 0.0
    rowIndex = 1

    enc.zero()
    driver.enable()

    while utime.ticks_diff(runtime, current_time) > 0:
        enc.update()
        current_position = enc.read()
        results[rowIndex, 2] = float(current_position)
        results[rowIndex, 1] = current_time

        duty = controller.run(current_position)
        motor.set_duty(duty)

        rowIndex +=1
        utime.sleep_ms(10)
        current_time = float((utime.ticks_ms() - offset)/1000)

    motor.set_duty(0)
    driver.disable()
    print("done")
    return test_results


if __name__ == '__main__':
    print("*** ME 405 Lab 2 ***")
    # initializing attached hardware
    hardware = initializeHardware()
    encoder = hardware[0]
    driver_m1 = hardware[1]
    m1 = hardware[2]
    controller = hardware[3]

    msgVisible = False
    testCounter = 0

    try:
        # Establishing serial communications with external PC
        external = initializeUART()

        while True:

            if (external.any() > 0):
                print("Reading data from COMPORT...",end='')
                test_params = readFrom(external)
                print("done")
                msgVisible = False

                gain = test_params[0]
                setpoint = test_params[1]

                # run the test loop and deal with timers in this function
                test_results = runControllerTest(gain, setpoint, encoder, driver_m1, m1, controller, testCounter)
                writeTo(external, test_results)
            else:
                if not msgVisible:
                    print("Waiting for input...")
                    msgVisible = True
                pass

    except KeyboardInterrupt:
        m1.set_duty(0)
        driver_m1.disable()
        print('leaving')