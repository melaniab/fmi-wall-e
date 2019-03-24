import serial
import time
import sys
import pickle

pickle_dir = "./pickle/motor_angles.pickle"
device = "/dev/ttyACM0"
rotate_motors = "RM {} {}\r"
move_motors = "DM {}\r"
stop_motors = "SM\r"
arguments_length = 3
move_command = "move"
rotate_command = "rotate"

#ser = serial.Serial(device,9600)
    
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
    

def send_rotate_command(motor_number,motor_angle):
    try:
        step = 5
        begin = 0
        end = 0
        last_motor_osses_dict = load_motors_last_angles()
        motor_number = int(motor_number)
        motor_angle= int(motor_angle)
        print('last',  last_motor_osses_dict)
        last_rotated_angle = last_motor_osses_dict[motor_number]
        if last_rotated_angle > motor_angle:
                begin = last_rotated_angle
                end = motor_angle
        else:
            begin = last_rotated_angle
            end = motor_angle
        if begin > end:
            step = -step
            
        for i in range(begin,end,step):
            command = rotate_motors.format(motor_number,i)
            send_signal_command(command)
            
        last_motor_osses_dict[motor_number] = motor_angle
        save_motors_last_angles(last_motor_osses_dict)
        print('new',  last_motor_osses_dict)
        
    except Exception as e:
        print(e)
        command = rotate_motors.format(motor_number,motor_angle)
        send_signal_command(command)



def send_signal_command(command):
    #ser.write(str.encode(command))
    print(command)

def parse():
    print(sys.argv)

    if sys.argv[1] == move_command:
        left_motor = sys.argv[2]
#        right_motor = sys.argv[3]
        command = move_motors.format(left_motor)
    elif sys.argv[1] == rotate_command:
        motor_number = sys.argv[2]
        motor_angle = sys.argv[3]
        send_rotate_command(motor_number,motor_angle)
    else:
        command = stop_motors
   


def save_motors_last_angles(a):
    with open(pickle_dir, 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_motors_last_angles():
    with open(pickle_dir, 'rb') as handle:
        b = pickle.load(handle)
        return b
    return None


if __name__ == "__main__":
    parse()
#    pass
   