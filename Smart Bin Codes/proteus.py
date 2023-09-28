import RPi.GPIO as GPIO
from time import sleep
import sys

c = 0;

# Define output pins
motor_channel = (29, 31, 33, 35)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Set pins to low
GPIO.setup(motor_channel, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# rotate_steps_cw = [[1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
# rotate_steps_acw = [[0, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0], [1, 0, 0, 1]]

number_of_steps = 1
max_steps = 1000

while True:

    # rotation = "cw"
    rotation = "cw";
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    c = 0;

    if GPIO.input(11) == GPIO.HIGH:
        if c == 0:

            rotation = "cw"
            c = 1;
            sleep(10)
            rotation = "acw"
            # c =0;

        elif c == 1:

            rotation = "acw"
            c = 0;

    if rotation == "cw":
        GPIO.output(motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
        sleep(0.02)
        GPIO.output(motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
        sleep(0.02)
        GPIO.output(motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
        sleep(0.02)
        GPIO.output(motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
        sleep(0.02)

    if rotation == "acw":
        GPIO.output(motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
        sleep(0.02)
        GPIO.output(motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
        sleep(0.02)
        GPIO.output(motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
        sleep(0.02)
        GPIO.output(motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
        sleep(0.02)

    number_of_steps += 1
    if number_of_steps == max_steps:
        GPIO.cleanup()
