import RPi.GPIO as gpio
import time
import tkinter as tk

dir1 = 7
pwm1 = 36
dir2 = 38
pwm2 = 15

gpio.setmode(gpio.BOARD)
i=0

gpio.setup(TRIG,gpio.OUT)
gpio.setup(ECHO,gpio.IN)
gpio.setup(11,gpio.OUT)
servo1 = gpio.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse
servo2 = gpio.pwm(13,50)

print("Calibrating.....")
time.sleep(0.1)

servo1.start(0.1)
servo2.start(0.1)
print ("Waiting for 2 seconds")
time.sleep(2)
# Define variable duty
duty = 2

#dir1, dir2 low for forward
#dir1, dir2 high for reverse
#dir1 is right, dir2 is left
#pwm1, pwm2 high for motors on/off

#pwm1 is right side motors
#pwm2 is left side motors

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(36, gpio.OUT)
    gpio.setup(38, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    gpio.setup(16, gpio.OUT)

def forward(tf):
    
    gpio.output(dir1, False)
    gpio.output(pwm1,True)
    gpio.output(dir2, False)
    gpio.output(pwm2,True)
    time.sleep(tf)
    gpio.cleanup()

def reverse(tf):
    
    gpio.output(dir1, True)
    gpio.output(pwm1,50)
    gpio.output(dir2, True)
    gpio.output(pwm2,50)
    time.sleep(tf)
    gpio.cleanup()

def left_turn(tf):
    
    gpio.output(dir2, True)
    gpio.output(pwm2,True)
    gpio.output(dir1, False)
    gpio.output(pwm1,True)
    time.sleep(tf)
    gpio.cleanup()

def right_turn(tf):
    
    gpio.output(dir2, False)
    gpio.output(pwm2,True)
    gpio.output(dir1, True)
    gpio.output(pwm1,True)
    time.sleep(tf)
    gpio.cleanup()

def servo_open(tf):
    servo1.ChangeDutyCycle(7)

def servo_close(tf):
    servo1.ChangeDutyCycle(2)

def servo_left(tf):
    servo2.ChangeDutyCycle(2)

def servo_centre(tf):
    servo2.ChangeDutyCycle(7)

def servo_right(tf):
    servo2.ChangeDutyCycle(12)

def key_input(event):
    init()
    print ("Key:", event.char)
    key_press = event.char
    sleep_time = 0.03

    if key_press.lower() == 'w':
        forward(sleep_time)
    elif key_press.lower() == 's':
        reverse(sleep_time)
    elif key_press.lower() == 'd':
        left_turn(sleep_time)
    elif key_press.lower() == 'a':
        right_turn(sleep_time)
    elif key_press.lower() == 'o':
        servo_open(sleep_time)
    elif key_press.lower() == 'c':
        servo_close(sleep_time)
    elif key_press.lower() == '4':
        servo_left(sleep_time)
    elif key_press.lower() == '8':
        servo_centre(sleep_time)
    elif key_press.lower() == '6':
        servo_right(sleep_time)
    
    else:
        print("Invalid key stroke")
        gpio.output(dir1,False)
        gpio.output(pwm1,False)
        gpio.output(dir2,False)
        gpio.output(pwm2,False)
    
command = tk.Tk()
command.bind('<KeyPress>', key_input)
command.mainloop()
