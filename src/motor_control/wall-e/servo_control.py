# This example moves a servo its full range (180 degrees by default) and then back.
from time import sleep
from signal import pause
from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

def verticaleMove(targetPosition):
    servo0 = servo.Servo(pca.channels[0])
    servo1 = servo.Servo(pca.channels[1])
    if(servo1.angle > 180):
        servo1.angle = 180

    if(servo1.angle < 0):
        servo1.angle = 0

    delta = 1
    if(servo1.angle > targetPosition):
        while(servo1.angle > targetPosition):
            if(servo1.angle > delta):
                servo1.angle -= delta
            else:
                servo1.angle = 0
            # sleep(0.1)
            servo0.angle = 180 - servo1.angle - 10
            # sleep(0.1)
    elif(servo1.angle < targetPosition):
        while(servo1.angle < targetPosition):
            if(servo1.angle < 180 - delta):
                servo1.angle += delta
            else:
                servo1.angle =180
            # sleep(0.1)
            servo0.angle = 180 - servo1.angle - 10
            # sleep(0.1)


def moveServo(index, targetPosition):
    if(index == 0 or index == 1):
        return

    currentServo = servo.Servo(pca.channels[index])
    print(currentServo.angle)
    print(targetPosition)
    if(currentServo.angle > 180):
        currentServo.angle = 180
    if(currentServo.angle < 0):
        currentServo.angle = 0

    if(currentServo.angle < targetPosition):
        while(currentServo.angle < targetPosition):
            print(currentServo.angle)
            print(targetPosition)
            if(currentServo.angle + 1 > targetPosition):
                currentServo.angle = targetPosition
                break;
            else:
                currentServo.angle += 1
    elif(currentServo.angle > targetPosition):
        while(currentServo.angle < targetPosition):
            if(currentServo.angle - 1 < targetPosition):
                currentServo.angle = targetPosition
                break;
            else:
                currentServo.angle -= 180


i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 100

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2480)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2400)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2600)

# The pulse range is 1000 - 2000 by default.
servo0 = servo.Servo(pca.channels[0])
servo1 = servo.Servo(pca.channels[1])
servo2 = servo.Servo(pca.channels[2])
servo3 = servo.Servo(pca.channels[3])
servo4 = servo.Servo(pca.channels[4])
servo5 = servo.Servo(pca.channels[5])
servo6 = servo.Servo(pca.channels[6])
servo7 = servo.Servo(pca.channels[7])

servo2.angle = 20
servo3.angle = 90
servo4.angle = 90
servo5.angle = 5
servo6.angle = 90
# servo7.angle = 90
# moveServo(7,80)
verticaleMove(90)

target = 110
# servo1.angle = 90
# servo0.angle = 180 - servo1.angle - 0
# sleep(1)



delta = 1 if servo1.angle < target else -1
print(target)
print(servo1.angle)
print(int(servo0.angle))
print(int(servo1.angle))
#for i in range(int(servo1.angle), target):
#    servo0.angle = 180 - i - 0
#    servo1.angle = i
#    sleep(0.05)
#    print(i)


# if(servo1.angle > 180):
#     servo1.angle = 180

# if(servo1.angle < 0):
#     servo1.angle = 0

# delta = 2
# if(servo1.angle > target):
#     while(servo1.angle > target):
#         if(servo1.angle > delta):
#             servo1.angle -= delta
#         else:
#             servo1.angle = 0
#         servo0.angle = 180 - servo1.angle - 0
# elif(servo1.angle < target):
#     while(servo1.angle < target):
#         if(servo1.angle < 180 - delta):
#             servo1.angle += delta
#         else:
#             servo1.angle =180
#         servo0.angle = 180 - servo1.angle - 10












