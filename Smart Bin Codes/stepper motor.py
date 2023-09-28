import RPi.GPIO as GPIO
import time
from machine import Pin
import utime
 
 #Define output pins
pin_a = pin(0, Pin.OUT)
pin_b = Pin(1, Pin.OUT)
pin_c = Pin(2, Pin.OUT)
pin_d = Pin(3, Pin.OUT)

 # Set pins to low
pin_a.low()
pin_b.low()
pin_c.low()
pin_d.low()

rotate_steps_cw = [[1,0,0,1],[1,1,0,0],[0,1,1,0],[0,0,1,1]]
rotate_steps_acw = [[0,0,1,1],[0,1,1,0],[1,1,0,0],[1,0,0,1]]

number_of_steps = 1
max_steps = 1000

button_cw = Pin(6, Pin.IN, Pin.PULL_DOWN)
button_acw = Pin(7, Pin.IN, Pin.PULL_DOWN)

rotation = "cw"

while True:

    if button_cw.value() == 1:
        rotation = "cw"
    
    if button_acw.value() ==1:
        rotation = "acw"
    
    if rotation == "cw":
        for step in rotate_steps_acw:
            pin_a.value(step[0])
            pin_b.value(stwp[1])
            pin_c.value(stwp[2])
            pin_d.value(stwp[3])
            utime.sleep(0.002)
    
    if rotation == "acw":
        for step in rotate_steps_acw:
            pin_a.value(step[0])
            pin_b.value(stwp[1])
            pin_c.value(stwp[2])
            pin_d.value(stwp[3])
            utime.sleep(0.002)
    
    
    number_of_steps += 1
    if number_of_steps == max_steps:
        pin_a.low()
        pin_b.low()
        pin_c.low()
        pin_d.low()

        break
