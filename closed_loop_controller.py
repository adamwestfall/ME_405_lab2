# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 08:32:30 2023

@author: conor
"""

#imports
import utime, encoder, motor_driver, pyb

class closed_loop_control:
    
    def __init__ (self, Kp, setpoint):
        
        self.Kp = Kp
        self.setpoint = setpoint
        
        
    def run(self, current_pos):
        
        # duty cycle or torque = Kp * (position_want - position_current)
        duty_cycle = self.Kp * (self.setpoint - current_pos)
        
        return duty_cycle
                    
    def set_setpoint(self, setpoint):
        
        self.setpoint = setpoint
                    
    def set_Kp(self, Kp):    
            
        self.Kp = Kp
 
 
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
    
    #Something to set Kp and initial setpoint
    init_Kp = 0
    init_setpoint = 0
    
    control_loop = closed_loop_control(init_Kp, init_setpoint)
    
    #While loop to continously run the controller
    try:
        while True:
            
            encoder_A.zero()
            Kp = float(input('Set Kp value:'))
            setpoint = int(input('Set setpoint value:'))
            
            control_loop.set_Kp(Kp)
            
            control_loop.set_setpoint(setpoint)
            
            time = []     
            position = []
            
            t_end = utime.time() + 2
            
            while utime.time() < t_end:
            
                #get position from encoder object
                encoder_A.update()
                current_pos = encoder_A.read()
                position.append(current_pos)
                time.append(utime.ticks_ms())
                pwm = control_loop.run(current_pos)
                m1.set_duty(pwm)
                
                #get time from utime.time()
                
            
                utime.sleep_ms(10)
                
            #print the output of time and position
            print(time)
            print(position)
            
        
    except KeyboardInterrupt:
        print('Program Terminated')
        m1.set_duty(0)
        
        
            
    
    