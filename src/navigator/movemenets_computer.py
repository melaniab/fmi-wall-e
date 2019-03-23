# horizontal_step: left <-> right step in degrees
# vertical_step: up <-> down step in degrees
# roi: rectangle of interest (the two points of the rectange)
def navigation_step(image_shape, center_point, horizontal_step=10, vertical_step=10):
  center_x, center_y = center_point
  h, w = image_shape
  
  # center_y < h/2 says that the object is below and we should go down
  vertical_direction = vertical_step if center_y < h/2 else -vertical_step
  # center_x < w/2 says that the object is on the left and we should go left
  horizontal_direction = horizontal_step if center_x < w/2 else -horizontal_step
  
  # No need to move
  if abs(center_y - h/2) / h < 0.05:
    vertical_direction = 0
  
  if abs(center_x - w/2) / w < 0.05:
     horizontal_direction = 0
  
  return vertical_direction, horizontal_direction

