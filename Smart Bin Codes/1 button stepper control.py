import RPi.GPIO as GPIO
import time
from machine import Pin
import utime
from time import sleep
 
 #Define output pins
pin_a = pin(29, Pin.OUT)
pin_b = Pin(31, Pin.OUT)
pin_c = Pin(33, Pin.OUT)
pin_d = Pin(35, Pin.OUT)

 # Set pins to low
pin_a.low()
pin_b.low()
pin_c.low()
pin_d.low()

rotate_steps_cw = [[1,0,0,1],[1,1,0,0],[0,1,1,0],[0,0,1,1]]
rotate_steps_acw = [[0,0,1,1],[0,1,1,0],[1,1,0,0],[1,0,0,1]]

number_of_steps = 1
max_steps = 1000

button_cw = Pin(11, Pin.IN, Pin.PULL_DOWN)
button_acw = Pin(7, Pin.IN, Pin.PULL_DOWN)

rotation = "cw"

while True:
    
    c = 0;
    if button_cw.value() == 1:
        if c ==0:
            rotation = "cw"
            c =1;
            time.sleep(10)
            rotation = "acw"
            #c =0;
            
        elif c==1:
            rotation = "acw"
            c=0;

    
    if rotation == "cw":
        for step in rotate_steps_acw:
            pin_a.value(step[0])
            pin_b.value(step[1])
            pin_c.value(step[2])
            pin_d.value(step[3])
            utime.sleep(0.002)
    

    if rotation == "acw":
        for step in rotate_steps_acw:
            pin_a.value(step[0])
            pin_b.value(step[1])
            pin_c.value(step[2])
            pin_d.value(step[3])
            utime.sleep(0.002)   
    
    
    number_of_steps += 1
    if number_of_steps == max_steps:
        pin_a.low()
        pin_b.low()
        pin_c.low()
        pin_d.low()

        break
