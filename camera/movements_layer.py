import sys
import os
import pickle
from pathlib import Path
import subprocess


movement_script = 'python3 /home/pi/Desktop/fmi-wall-e/camera/raspberry_to_arduino.py {}'
STATE_PATH = '/home/pi/Desktop/fmi-wall-e/camera/state.pickle'

STATE_BEGINNIG = {
    0: 90,
    1: 90,
    2: 35,
    3: 90,
    4: 115,
    5: 0,
    6: 0,
    7: 90,
}

def load_state_walle():
    state_file = Path(STATE_PATH)
    if not state_file.exists():
        save_state_walle(STATE_BEGINNIG)
        return STATE_BEGINNIG    

    with open(STATE_PATH, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data


def save_state_walle(state):
    with open(STATE_PATH, 'wb') as handle:
        pickle.dump(state, handle, protocol=pickle.HIGHEST_PROTOCOL)


def execute_sh_command(args):
    print(movement_script.format(args))
    os.system(movement_script.format(args))


def move_forward(distance):
    execute_sh_command('move 50')


def move_motor(state, motor, relative_degrees):
    state[motor] += relative_degrees
    degrees = state[motor]
    degrees = min(180, max(0, degrees)) 
    command = 'RM {} {}'.format(motor, degrees)
    execute_sh_command(command)


def move_claw(action):
    motor = 5
    if action == 'OPEN':
        degrees = '50'
    elif action == 'CLOSE':
        degrees = '0'
    command = 'RM {} {}'.format(motor, degrees)
    execute_sh_command(command)


if __name__ == "__main__":
    state = load_state_walle()

    if sys.argv[1] == 'MOVE_BODY_FORWARD':
        move_forward(None)

    elif sys.argv[1] == 'MOVE_HORIZONTAL':
        motor = 7
        relative_degrees = sys.argv[2]
        move_motor(state, motor, relative_degrees)

    elif sys.argv[1] == 'MOVE_VERTICAL':
        pass
    
    elif sys.argv[1] == 'ORIENT_CLAW':
        motor = 6
        relative_degrees = sys.argv[2]
        move_motor(state, motor, relative_degrees)

    elif sys.argv[1] == 'MOVE_CLAW':
        action = sys.argv[2]
        move_claw(action)

    save_state_walle(state)
