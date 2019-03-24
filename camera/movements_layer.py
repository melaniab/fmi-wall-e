import sys
import os
import pickle
from pathlib import Path



movement_script = '/home/pi/Desktop/fmi-wall-e/camera/raspberry_to_arduino.py {}'
STATE_PATH = '/home/pi/Desktop/fmi-wall-e/camera/state.pickle'
AXIS_MOTOR_MAPPING = {
    'AXIS_0': 7
}
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
    os.system(movement_script.format(args))


def move_forward(distance):
    execute_sh_command('move 50')


def move_axis(state, axis, relative_degrees):
    motor = AXIS_MOTOR_MAPPING[axis]
    state[motor] += relative_degrees
    command = 'RM {} {}'.format(motor, state[motor])
    execute_sh_command(command)


def move():
    state = load_state_walle()
    move_forward(None)
    save_state_walle(state)

if __name__ == "__main__":
    move()
