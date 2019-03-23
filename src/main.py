import logging
from image_processing import model_initializer
from remote_communication.remote_communicator import get_image_dir
from navigator.detection_n_orientation import *
from navigator.navigator import *
from locator import distance_computer
from navigator.detection_n_orientation import *


if __name__ == "__main__":
    model = model_initializer.load_model()

    # Somehow we have to know whether
    # Wall-E has collected the trash.
    while True:
        image_dir = get_image_dir()
        print(image_dir)
        mask = get_mask(model, image_dir)
        distance_to_object = distance_computer.get_distance()

        move_command = move(mask)
        print(move_command)
        logging.info('Command for the movement {}'.format(move_command))
        if move_command == MOVE_CLAW:
            break
