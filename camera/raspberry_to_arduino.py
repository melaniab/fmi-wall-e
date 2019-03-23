import serial
import time
import sys

device = "/dev/ttyACM0"
rotate_motors = "RM {} {}\r"
move_motors = "DM {}\r"
stop_motors = "SM\r"
arguments_length = 3
move_command = "move"
rotate_command = "rotate"

initialization_motor_osses = {
    1 :90,
    2 :90,
    2 :90,
    3 :90,
    4 :90,
    5 :90,
    6 :90,
    7 :90
    }

last_motor_osses = {
    1 :90,
    2 :90,
    2 :90,
    3 :90,
    4 :90,
    5 :90,
    6 :90,
    7 :90
    }




ser = serial.Serial(device,9600)
#ser.write(str.encode('a'))
#for i in range(0,100):
#   ser.write(str.encode('a'))
#   time.sleep(1)
# 

def parse_arguments():
    print(sys.argv)
#    if len(sys.argv) < arguments_length:
#        return
    
    command = "command"

    if sys.argv[1] == move_command:
        left_motor = sys.argv[2]
#        right_motor = sys.argv[3]
        command = move_motors.format(left_motor)
    elif sys.argv[1] == rotate_command:
        motor_number = sys.argv[2]
        motor_angle = sys.argv[3]
        command = rotate_motors.format(motor_number,motor_angle)
    else:
        command = stop_motors
    print(command)
    return command
    

def send_command():
    command = parse_arguments()
    print("i will send this command {}".format(command))
    ser.write(str.encode(command))
    

def stop_motors_command():
    command = stop_motors
    send_signal_command(command)

def move_motors_command(left_motor,right_motor):
    stop_motors_after = 1
    command = move_motors.format(left_motor)
    send_signal_command(command)
    time.sleep(stop_motors_after)
    stop_motors_command()
    

def send_rotate_commands(motor_number,motor_angle):
    step = 5
    begin = 0
    end = 0
    last_rotated_os = last_motor_osses[motor_number]
    if last_rotated_os > motor_angle:
            step = -step
            begin = last_rotated_os
            end = motor_angle
    else:
        begin = motor_angle
        end = last_rotated_os
        
    for i in range(begin,end,step):
        command = rotate_motors.format(motor_number,i)
#    
    pass




def send_signal_command(command):
    ser.write(str.encode(command))


def parse_arguments_new_function():
    print(sys.argv)
#    if len(sys.argv) < arguments_length:
#        return
    
    command = "command"

    if sys.argv[1] == move_command:
        left_motor = sys.argv[2]
#        right_motor = sys.argv[3]
        command = move_motors.format(left_motor)
    elif sys.argv[1] == rotate_command:
        motor_number = sys.argv[2]
        motor_angle = sys.argv[3]
        command = rotate_motors.format(motor_number,motor_angle)
    else:
        command = stop_motors
    print(command)
    return command




if __name__ == "__main__":
    send_command()
#    pass