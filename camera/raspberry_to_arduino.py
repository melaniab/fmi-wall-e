import serial
import time

device = "/dev/ttyUSB1"

ser = serial.Serial(device,9600)
ser.write(str.encode('a'))


for i in range(0,100):
   ser.write(str.encode('a'))
   time.sleep(1)
 


