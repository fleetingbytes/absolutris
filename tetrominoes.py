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
        self.current_rotation = self.r0
        self.spawn_offset = 0
    def __call__(self):
        return self.current_rotation()


class Tetromino_I(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((-1, 0), (1, 0), (2, 0)), 
                           Rotated_Shape((0, 1), (0, -1), (0, -2)),
                           Rotated_Shape((1, 0), (-1, 0), (-2, 0)), 
                           Rotated_Shape((0, -1), (0, 1), (0, 2)),
                           )
    def __call__(self):
        return super().__call__()


class Tetromino_J(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((-1, 0), (1, 0), (1, 1)),
                           Rotated_Shape((0, 1), (0, -1), (-1, 1)),
                           Rotated_Shape((1, 0), (-1, 0), (-1, -1)),
                           Rotated_Shape((0, -1), (0, 1), (-1, 1)),
                           )
        self.spawn_offset = -1
    def __call__(self):
        return super().__call__()


class Tetromino_L(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((1, 0), (-1, 0), (-1, 1)),
                           Rotated_Shape((0, -1), (0, 1), (1, 1)),
                           Rotated_Shape((-1, 0), (1, 0), (1, -1)),
                           Rotated_Shape((0, 1), (0, -1), (-1, -1)),
                           )
        self.spawn_offset = -1
    def __call__(self):
        return super().__call__()


class Tetromino_O(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((1, 0), (1, -1), (0, -1)),
                           Rotated_Shape((0, -1), (-1, -1), (-1, 0)),
                           Rotated_Shape((-1, 0), (-1, 1), (0, 1)),
                           Rotated_Shape((0, 1), (1, 1), (1, 0)),
                           )
    def __call__(self):
        return super().__call__()


class Tetromino_S(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((-1, 0), (0, -1), (1, -1)),
                           Rotated_Shape((0, 1), (-1, 0), (-1, -1)),
                           Rotated_Shape((1, 0), (0, 1), (-1, 1)),
                           Rotated_Shape((0, -1), (1, 0), (1, 1)),
                           )
    def __call__(self):
        return super().__call__()


class Tetromino_T(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((0, 1), (-1, 0), (1, 0)),
                           Rotated_Shape((1, 0), (0, 1), (0, -1)),
                           Rotated_Shape((0, -1), (1, 0), (-1, 0)),
                           Rotated_Shape((-1, 0), (0, -1), (0, 1)),
                           )
        self.spawn_offset = -1
    def __call__(self):
        return super().__call__()


class Tetromino_Z(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        Tetromino.__init__(self, 
                           Rotated_Shape((1, 0), (0, -1), (-1, -1)),
                           Rotated_Shape((0, -1), (-1, 0), (-1, 1)),
                           Rotated_Shape((-1, 0), (0, 1), (1, 1)),
                           Rotated_Shape((0, 1), (1, 0), (1, -1)),
                           )
    def __call__(self):
        return super().__call__()


if __name__ == "__main__":
    pass
