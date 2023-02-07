# -*- coding: utf-8 -*-
"""
Created on  Feb 6 2023

@author: Conor Fraser
@author: Adam Westfall
@author: Jason Davis

"""

import utime, encoder, motor_driver, pyb, closed_loop_controller

if __name__ == '__main__':
    #enable any motor and encoder pins, probaby imported    
    enable1 = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    input1 = pyb.Pin.cpu.B4
    input2 = pyb.Pin.cpu.B5
    
    timer1 = pyb.Timer(3, freq = 20000) 

    #creating motor driver / motor objects
    # enable pin, input1, input2, timer
    m1_driver = motor_driver.MotorDriver(enable1, input1, input2, timer1)
    m1 = m1_driver.motor(input1, input2, 1, 2, "MOTOR A")
    
    encoder_A = encoder.Encoder(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4, ID="ENCODER A")
    
    # turning on the motor
    m1_driver.enable()
    
    # setting motor
    #m1.set_duty(75)
    # zero encoder
    encoder_A.zero()
    
    # create the virtual com port
    u2 = pyb.UART(2, baudrate=115200)
        
        
    # wait for characters to be available

    
    #While loop to continously run the controller
    try:
        while True:

            encoder_A.zero()
            
            try:
                while not u2.any():
                    pass
                charIn = u2.readline()
                print(charIn)
                charIn.strip('\n\r')
                line = charIn.split(',')
                print(line)
                print('hjere')
                Kp = float(line[0])
                setpoint = int(line[1])
                
            except TypeError:
                print('invalid kp or setpoint recieved')
                
            control_loop = closed_loop_controller.closed_loop_control(Kp, setpoint)
            encoder_A.zero()
            
            time = []     
            position = []
            
            t_end = utime.time() + 2
            
            while utime.time() < t_end:
            
                encoder_A.update()
                current_pos = encoder_A.read()
                position.append(current_pos)
                time.append(utime.ticks_ms())
                pwm = control_loop.run(current_pos)
                m1.set_duty(pwm)
                
            
                utime.sleep_ms(10)
                
            # print the output of time and position

            


            # TODO: take the time and position outputs and put them in a csv format
            for i in len(time):
                data = f"{time[i]},{position[i]}\n\r"
                u2.write(data)
            u2.write('done\n\r')
            

            
            
        
    except KeyboardInterrupt:
        print('Program Terminated')
        m1.set_duty(0)