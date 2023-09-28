import RPi.GPIO as GPIO
import time
from machine import Pin
import utime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 18
ECHO = 24
led = 4

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(led,GPIO.OUT)
 
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
    GPIO.output(TRIG, False)

    time.sleep(1)

    GPIO.output(TRIG, True)
    time.sleep(0.01)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start=time.time()

    while GPIO.input(ECHO)==1:
        pulse_end=time.time()

    pulse_duration=pulse_end-pulse_start

    distance = pulse_duration*11150
    distance = round(distance,2)
    
    c = 0;
    if button_cw.value() == 1:
        if c ==0:
            rotation = "cw"
            c =1;

    elif button_cw.value() == 1:
        if c==1:
            rotation = "acw"
            c=0;
    
    elif button_cw.value() == 0:
        if c==1:
            time.sleep(10)
            rotation = "acw"
            c=0;
    
    if c==0:    
        if distance < 5:
            if button_cw.value() == 1:
                    print("Dustbin is full!");
                    #break
                                



    
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
