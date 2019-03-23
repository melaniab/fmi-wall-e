import logging
from image_processing import model_initializer
from remote_communication import image_collector
from navigator.detection_n_orientation import *
from navigator.navigator import move
from locator import distance_computer, stop_condition

if __name__ == "__main__":
    model = model_initializer.load_model()

    # Somehow we have to know whether
    # Wall-E has collected the trash.
    while False:
        image_dir = image_collector.get_image()
        mask = get_mask(model, image_dir)
        distance_to_object = distance_computer.get_distance()

        move_command = move(mask, distance_to_object)
        logging.info('Command for the movement {}'.format(move_command))

        if stop_condition():
            break

    