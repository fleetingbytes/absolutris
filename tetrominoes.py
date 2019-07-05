from pygame import Surface
from pygame import image

class Rotated_Shape():
    """
    Each rotation of each Tetromino is defined as an instance
    of Rotated_Shape. The referece tile of a tetromino is 
    always (0, 0) and thus omitted.
    """
    def __init__(self, tile1: tuple, tile2: tuple, tile3: tuple) -> None:
        self.tile1x, self.tile1y = tile1
        self.tile2x, self.tile2y = tile2
        self.tile3x, self.tile3y = tile3
        self.xdim = max((self.tile1x, self.tile2x, self.tile3x)) - min((self.tile1x, self.tile2x, self.tile3x)) + 1
        self.ydim = max((self.tile1y, self.tile2y, self.tile3y)) - min((self.tile1y, self.tile2y, self.tile3y)) + 1
        self.size = (self.xdim, self.ydim)
    def __call__(self):
        return ((0, 0), (self.tile1x, self.tile1y), (self.tile2x, self.tile2y), (self.tile3x, self.tile3y))


class Tetromino():
    def __init__(self, 
                 r0: Rotated_Shape, 
                 r90: Rotated_Shape, 
                 r180: Rotated_Shape, 
                 r270: Rotated_Shape) -> None:
        self.r0 = r0
        self.r90 = r90
        self.r180 = r180
        self.r270 = r270


I0 = Rotated_Shape((-1, 0), (1, 0), (2, 0))
I90 = Rotated_Shape((0, 1), (0, -1), (0, -2))
I180 = Rotated_Shape((1, 0), (-1, 0), (-2, 0))
I270 = Rotated_Shape((0, -1), (0, 1), (0, 2))

J0 = Rotated_Shape((1, 0), (-1, 0), (-1, -1))
J90 = Rotated_Shape((0, -1), (0, 1), (-1, 1))
J180 = Rotated_Shape((-1, 0), (1, 0), (1, 1))
J270 = Rotated_Shape((0, 1), (0, -1), (1, -1))

L0 = Rotated_Shape((1, 0), (-1, 0), (-1, 1))
L90 = Rotated_Shape((0, -1), (0, 1), (1, 1))
L180 = Rotated_Shape((-1, 0), (1, 0), (1, -1))
L270 = Rotated_Shape((0, 1), (0, -1), (-1, -1))

O0 = Rotated_Shape((1, 0), (1, -1), (0, -1))
O90 = Rotated_Shape((0, -1), (-1, -1), (-1, 0))
O180 = Rotated_Shape((-1, 0), (-1, 1), (0, 1))
O270 = Rotated_Shape((0, 1), (1, 1), (1, 0))

S0 = Rotated_Shape((-1, 0), (0, -1), (1, -1))
S90 = Rotated_Shape((0, 1), (-1, 0), (-1, -1))
S180 = Rotated_Shape((1, 0), (0, 1), (-1, 1))
S270 = Rotated_Shape((0, -1), (1, 0), (1, 1))

T0 = Rotated_Shape((0, 1), (-1, 0), (1, 0))
T90 = Rotated_Shape((1, 0), (0, 1), (0, -1))
T180 = Rotated_Shape((0, -1), (1, 0), (-1, 0))
T270 = Rotated_Shape((-1, 0), (0, -1), (0, 1))

Z0 = Rotated_Shape((1, 0), (0, -1), (-1, -1))
Z90 = Rotated_Shape((0, -1), (-1, 0), (-1, 1))
Z180 = Rotated_Shape((-1, 0), (0, 1), (1, 1))
Z270 = Rotated_Shape((0, 1), (1, 0), (1, -1))

class TetrominoI(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, I0, I90, I180, I270)


if __name__ == "__main__":
    pass