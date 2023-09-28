import RPi.GPIO as GPIO
import time
import sys
from Tkinter import *
import tkFont

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

in1 = 17
in2 = 18
in3 = 27
in4 = 22
TRIG = 23
ECHO = 24

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002
 
step_count = 1024 # 5.625*(1/64) per step, 4096 steps is 360°
 
c=1
j=0 
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
 
# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( TRIG, GPIO.OUT)
GPIO.setup( ECHO, GPIO.IN)

#LCD screen:
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output(TRIG, False) 
#GPIO.setup(4, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
#GPIO.setup(10, GPIO.IN,  pull_up_down=GPIO.PUD_UP)

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;
 
 
def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()
 
     
# THE MEAT


win = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')


def openProgram():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance+1.15, 2)

    if distance<=5:
        print "DUSTBIN IS FULL"
        bottom = Tk()  
        text = Text(bottom)  
        text.insert(INSERT, "Dustbin is Full")  
        j=1
        
    if distance>5:
        print "USE ME"
        bottom = Tk()  
        text = Text(bottom)  
        text.insert(INSERT, "USE ME!")
        j=0
    time.sleep(2)

    print("Open button pressed")
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep( step_sleep )
    
    time.sleep(3)
    val1 = hx.get_weight(5)
    print(f"val1={val1}")
    hx.power_down()
    hx.power_up()
    f = open("data.csv","a+")    
    f.write("\n")
    f.write(str(val1))
    f.write("\n")
    f.close() 
    time.sleep(2)   
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep( step_sleep)

        
def exitProgram():
    print("Exit Button pressed")
        GPIO.cleanup()
    win.quit()	

def sense_level():

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance+1.15, 2)

    if distance<=5:
        print "DUSTBIN IS FULL"
        j=1
        
    if distance>5:
        print "USE ME"
        j=0
    time.sleep(2)

win.title("Smart Bin")
win.geometry('800x480')

exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =2 , width = 6) 
exitButton.pack(side = BOTTOM)

bin_open = Button(win, text = "OPEN", font = myFont, command = openProgram, height = 2, width =8 )
bin_open.pack()

mainloop()