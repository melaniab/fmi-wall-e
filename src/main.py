import logging
from image_processing import model_initializer
from remote_communication.remote_communicator import get_image_dir, move_remote
from navigator.detection_n_orientation import *
from navigator.navigator import *
from locator import distance_computer
from navigator.detection_n_orientation import *


if __name__ == "__main__":
    move_remote('INITIALIZE', '')
    model, visualize = model_initializer.load_model()

    # Somehow we have to know whether
    # Wall-E has collected the trash.
    while True:
        image_dir = get_image_dir()
        print('Processing image: {}'.format(image_dir))
        mask = get_mask(model, image_dir, visualize)
        distance_to_object = distance_computer.get_distance()

        move_commands = move(mask)
        ssh = None
        for move_command, arg in move_commands:
            ssh = move_remote(move_command, arg)
            logging.info('Command for the movement {} with args {}'.format(move_command, arg))
            print('Command for the movement {} with args {}'.format(move_command, arg))

        if move_commands[-1] == (MOVE_CLAW, CLOSE):
            break
