import detection_n_orientation
import movemenets_computer

# TODO: extract constants to somewhere...
# TODO: metrics?
MIN_DISTANCE = 10

# Returns a command for Wall-E in the format
# COMMAND, ARGS FOR COMMAND, CENTER_POINT
# where CENTER_POINT is the center of the object
def move(mask, distance_to_object):
    degrees, center_point = detection_n_orientation.calculate_center_angle(mask)
    image_shape = mask.shape

    if distance_to_object <= MIN_DISTANCE:
        # In this case we have to move the CLAW!
        return 'MOVE_CLAW', degrees, center_point

    # In this case we are moving the HAND!
    vertical_direction, horizontal_direction = movemenets_computer.navigation_step(image_shape, center_point)
    return 'MOVE_HAND', (vertical_direction, horizontal_direction), center_point
