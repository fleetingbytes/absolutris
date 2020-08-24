# Absolutris

Implementation of tetris in pygame

### Display Info

Answer:
The common factors are:
1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120

The Greatest Common Factor:
GCF = 120

Solution
The factors of 1080 are:
1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 27, 30, 36, 40, 45, 54, 60, 72, 90, 108, 120, 135, 180, 216, 270, 360, 540, 1080

The factors of 1920 are:
1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 30, 32, 40, 48, 60, 64, 80, 96, 120, 128, 160, 192, 240, 320, 384, 480, 640, 960, 1920

The common factors are:
1	1920x1080
2	960x540
3	640x360
4	480x270
5	384x216
6	320x180
8	240x135
10	192x108
12	160x90
15	128x72
20	96x54
24	80x45
30	64x36
40	48x27
60	32x18
120	16x9

The Greatest Common Factor:
GCF = 120


### Mino Production Pipeline

#### Generator

* Each generator module defines a `source()` function which returns a generator of base-7 numbers, i.e. it yields integers 0, 1, 2, 3, 4, 5, or 6.
* If the generator is ever depleted it shall follow Python's standard generator behavior and return None which raises StopIteration.
* The generator must be able to react to GeneratorExit thrown to it from the caller.

#### Packer

* The packer pulls the minoes represented as integers from the random source generator and groups them into groups. It may apply certain rules imposed on groups. For example, certain tetris variants may require that minoes are drawn in a random order from a bag containing all seven types of minoes. To achieve this, a packer can draw minoes from the random source ignoring multiple instances of a mino type until it builds a sequence of all seven mino types. Another way of achieving this would be to ignore the random source generator completely, creating the seven minoes in the packer and shuffling them at random.

* The packer is an optional link in the pipeline and can be omitted.

#### Next Window

* The next window is an abstract representation of the window showing a preview of one or more minoes which will be spawned next.
* The next window pulls minoes represented as base-7 integers from either a packer or a random source.
* The number of pieces shown in the next window is defined in the level properties.
* The next window is an optional link in the pipeline and can be omitted.

#### Playfield

* The playfield pulls minoes one by one from the next window and spawns them in the spawn point on the playfield.
* The player plays and places the mino.
* The playfield sends minoes and other events (key presses, game ticks, game steps, etc.) to the history recorder

#### History Recorder

* The history recorder records various events in the game. Among other things it receives and records the lifetime of minoes on the playfield.
* The history recorder processes the events and sends information to the statistics.

#### Statistics

* The statistics accumulate and display data from the history recorder. For example which minoes were spawned on the playfield, how they were played, when and how they were cleared.
