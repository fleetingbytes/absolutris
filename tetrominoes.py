# This module defines the classes of tetrominoes and their shape
#
# 1. The concept of a tetromino
#
#   We distinguish between a tile and a mino. A tile is the smallest element of the tetris playfield, 
#   analogous to a pixel of a screen. A tile is a direct subsurface of the pygame.display surface.
#   In the course of the game a tile instance blits various pygame.surfaces (loaded images) into 
#   the dipslay surface.
#   A tetromino is a brick composed of four minoes. Each mino is orthogonally adjacent to another.
#   Each tetromino is one of the possible arrangements of four minoes. The tetrominoes are 
#   called by the capital letters of the latin alphabet they resemble: I, J, L, O, S, T, Z.
#   capital letters of the latin alphabet.
#   A tetromino always occupies four tiles of the playfield. Each tile is occupied by one of
#   the tetrominoes minoes. (The tile instance holds the mino.)
# 
#   The player can rotate the tetrominoes in 90° steps. Because of 

from pygame import Surface
from pygame import image

class Mino():
    """
    A mino is the building block of tetrominoes.
    """
    def __init__(self, forward: int, left: int):
        self.forward = forward
        self.left = left
        self.rotate(0)
        # self.rotate() defines:
        # self.column
        # self.row
    def rotate(self, rotation: int):
        # we rotate by n times 90°
        if rotation == 0:
            self.column = self.left
            self.row = self.forward
        elif rotation == 1:
            self.column = self.forward
            self.row = -self.left
        elif rotation == 2:
            self.column = -self.left
            self.row = -self.forward
        elif rotation == 3:
            self.column = -self.forward
            self.row = self.left
    def __iter__(self):
        return iter(tuple((self.column, self.row)))
    def __repr__(self):
        return f"Mino(col={self.column}, row={self.row})"


class Tetromino():
    """
    A tetromino is a configuration of four adjacent minoes.
    """
    def __init__(self, mino_1: Mino, mino_2: Mino, mino_3: Mino) -> None:
        self.mino_0 = Mino(0, 0)
        self.mino_1 = mino_1
        self.mino_2 = mino_2
        self.mino_3 = mino_3
        self.current_rotation = 0
        self.rotate(self.current_rotation)
        self.spawn_offset = 0
    def __iter__(self):
        return iter(tuple((self.mino_0, self.mino_1, self.mino_2, self.mino_3)))
    def __repr__(self):
        return f"Tetromino({self.mino_0.column}, {self.mino_0.row}), {self.mino_1.column}, {self.mino_row}), {self.mino_2.column}, {self.mino_2.row}, {self.mino_3.column}, {self.mino_3.row})" 
    def rotate(self, n: int):
        for mino in self:
            mino.rotate(n)
        self.current_rotation = n


class Tetromino_I(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, 1), Mino(0, 2), Mino(0, -1))

class Tetromino_J(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, 1), Mino(0, -1), Mino(1, 1))
        self.spawn_offset = -1

class Tetromino_L(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, 1), Mino(0, -1), Mino(1, -1))
        self.spawn_offset = -1

class Tetromino_O(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, 1), Mino(-1, 0), Mino(-1, 1))

class Tetromino_S(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, -1), Mino(-1, 0), Mino(-1, 1))

class Tetromino_T(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, 1), Mino(0, -1), Mino(1, 0))
        self.spawn_offset = -1


class Tetromino_Z(Tetromino):
    def __init__(self):
        self.img = image.load("img/pattern.png")
        super().__init__(Mino(0, 1), Mino(-1, 0), Mino(-1, -1))


mapping = {0: Tetromino_I,
           1: Tetromino_J,
           2: Tetromino_L,
           3: Tetromino_O,
           4: Tetromino_S,
           5: Tetromino_T,
           6: Tetromino_Z}


if __name__ == "__main__":
    pass
