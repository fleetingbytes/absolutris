import pygame
import numpy
import random

# it is possible to create a pygame.Color from a tuple of values:
random_values = tuple((random.randint(0, 255) for _ in range(4)))
color = pygame.Color(*random_values)
print(f"successfully created pygame.Color: {color}")

# now for some real application
pixel_color = pygame.Color(2795939583)
print(f"pixel color: {pixel_color}")

# planning to change the intensity of the individual color channels R, G, B, A:
intensity = 25
factors = (1, -1, 1, 0)

# the following will add or subtract 25 from each channel in the pixel_color (while keeping them in range [0,255]):
# pixel_color:     (166, 166, 166, 0)
# relative change: (+25, -25, +25, 0)
# resulting color: (191, 141, 191, 0)
numpy_values = tuple(max(min(255, channel + (intensity * factor)), 0) for channel, factor in zip(pixel_color, factors))
print(f"numpy values: {numpy_values}")
new_pixel_color = pygame.Color(*numpy_values)
