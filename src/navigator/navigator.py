import navigator.detection_n_orientation as detection_n_orientation
import navigator.movemenets_computer as movemenets_computer
import numpy as np

# TODO: extract constants to somewhere...
# TODO: metrics?

THRESHOLD_COVERAGE = 0.001
THRESHOLD_ANGLE = 5

MOVE_AXIS_0 = 'MOVE_AXIS_0'
MOVE_AXIS_1 = 'MOVE_AXIS_1'
MOVE_AXIS_2 = 'MOVE_AXIS_2'
MOVE_BODY_FORWARD = 'MOVE_BODY_FORWARD'
MOVE_CLAW = 'MOVE_CLAW'
FORWARD_DISTANCE_LONG = 10 #e.g. cm
FORWARD_DISTANCE_CLOSE = 3

# Calculate what part of the image the cigarette covers.
def calculate_coverage(mask):
    return mask.reshape(-1).sum() / len(mask.reshape(-1))


# Returns a command for Wall-E in the format
# COMMAND, ARGS FOR COMMAND
def move(mask):
    if mask is None:
        # Wall-E hasn't discovered a cigarrette.
        # We should move.
        return [(MOVE_BODY, FORWARD_DISTANCE_LONG)]

    degrees, center_point = detection_n_orientation.calculate_center_angle(mask)
    image_shape = mask.shape

    vertical_direction, horizontal_direction = movemenets_computer.navigation_step(image_shape, center_point)
    coverage = calculate_coverage(mask)
    print(coverage)

    if coverage <= THRESHOLD_COVERAGE and (vertical_direction == 0 or horizontal_direction == 0):
        # We are not close enough but we are centered
        # We should move
        return [(MOVE_BODY, FORWARD_DISTANCE_CLOSE)]

    elif coverage <= THRESHOLD_COVERAGE:
        # We are not close enough and neither are we centered
        # First, we'll try to center the image.
        return [(MOVE_AXIS_0, horizontal_direction),  (MOVE_AXIS_1, vertical_direction)]

    # We are close enough
    if degrees > THRESHOLD_ANGLE and degrees < 180 - THRESHOLD_ANGLE:
        # Orienting the claw.
        return [(MOVE_AXIS_2, THRESHOLD_ANGLE)]

    # Try to catch.
    return [(MOVE_CLAW, '')]
