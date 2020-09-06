# Recording

The game of Absolutris can be recorded in a file. As the Recorder processes the game events to record, it creates and updates a Statistics object in memory. When a recorded game is replayed a Replayer reads the recorded data from a file and creates and updates a Statistics object.

## Structure of Recorded Data

The file with recorded data consists of a header, body, and a footer.

### Header

The Header contains the information about the playfield and game plan serialized as follows:

* Begin header separator
* Playfield width
* Playfield height
* Plan name
* Plan version
* End header separator
* Begin data separator

### Body

The Body contains binary data

* Data block

### Footer

The Footer signifies the end of the file
* End data separator

## Encoding of the Recorded Data

Header and footer are human-readable text encoded in UTF-8. Data block is binary data.

### Header Format Specification

-----BEGIN ABSOLUTRIS GAME METADATA-----
Playfield width: 10
Playfield height: 20
Plan name: default
Plan version: 0.0.1
-----END ABSOLUTRIS GAME METADATA-----
-----BEGIN ABSOLUTRIS GAME DATA-----

### Footer Format Specification

-----END ABSOLUTRIS GAME DATA-----

### Data Block Structure

#### Next Window Content

Data Block starts with the sequence of pieces in the Next Window. 

#### Frames

Each frame of the game is recorded as a block of 1 or more bits. 

### Data Block Encoding

#### Next Window Content Encoding

Each tetromino in the Next Window is represented by three bits. The Game Plan provides information on how many tetrominoes are in the next window. The tetromino mapping is motivated by the similarity of the shape arabic numbers 0, 1, 2, 3, 4, 5, 6 with the shape of tetrominoes:

* O: 0
* I: 1
* L: 2
* T: 3
* Z: 4
* S: 5
* J: 6

A game plan with Next Window length of 4 will produce 12 bits of data.

#### Frame Encoding

A frame with no events is recorded as bit 0.  A frame with some events is recorded as bit 1 followed by a variable number of bits.

##### Event Information

A frame can only bear one event. It is one of:

* Spawning a tetromino
* Tetromino manipulation:
		* Changing row
		* Changing column
		* Changing rotation
		* Locking a tetromino (or hard-dropping)

Changing the row, column, or rotation can be combined if such moves were issued in one of the previous frames but could not be performed before (because of local restrictions).

The number of bits encoding the frame information can be implied from the event type as follows:

Read three bits. If they don't equal 0b111, then this is a spawning event (or ending game if spawned into an occupied tile). Else (if they equal 0b111) this is a tetromino manipulation frame.

###### Spawning a tetromino

If a tetromino is spawned, the binary value of the three bits represents the spawned tetromino. If the Game Plan has a visible Next Window, the following three bits represent the newes member of the Next Window.

Example of a spawn event in a game plan with visible Next Window (of any length):

                 1 100 011
                 ^  ^   ^
                 |  |   |
    Eventful Frame  |   Tetromino T appended at the end of the Next Window
                    |
           Spawned Tetromino Z

Example of a spawn event in a game plan without visible Next Window:

                 1 100
                 ^  ^
                 |  |
    Eventful Frame  Tetromino Z spawned

###### Tetromino manipulation

Tetromino manipulation event is marked by the bits 0b111 followed by a bitfield of another three bits with information about the manipulation type:

                 1 111 1 0 0 (...)
                 ^  ^  ^ ^ ^
                 |  |  | | |
    Eventful Frame  |  | | Bit indicating whether rotation was changed.
                    |  | |
                    |  | Bit indicating whether column was changed.
                    |  |
                    |  Bit indicating whether row was changed.
                    |
    Manipulating previously spawned tetromino

Manipulation types and implications for following data:

* 0b000 - hard-drop (and lock) tetromino -> No further bits to read
* 0b100 - row changed -> read 5 more bits, the binary representation of the row number
* 0b010 - column changed -> read 4 more bits, the binary representation of the column number
* 0b001 - rotation changed -> read 2 more bits, encoding one of four possible rotations
* 0b110 - row and column changed -> read 5 bits for row and then 4 more bits for column
* 0b101 - row and rotation changed -> read 5 bits for row and then 2 more bits for rotation
* 0b011 - column and rotation changed -> read 4 bits for column and then 2 more bits for rotation
* 0b111 - row, column and rotation changed -> read 5 bits for row, 4 bits for column and then 2 more bits for rotation

Thus an eventful frame is encoded with a total of 7, 9, 11, 12, 13, 14, 16, or 18 bits. The longest possible frame information look like this:


                 1 111 111 01101 1010 01
                 ^  ^   ^    ^     ^   ^
                 |  |   |    |     |   |
    Eventful frame  |   |    |     |   Change rotation to: West
                    |   |    |     |
                    |   |    |     Position piece in column 10
                    |   |    |
                    |   |    Position piece in row 13
                    |   |
                    |   Bitfield indicating what changed (row, column, and rotation)
                    |
    Manipulating previously spawned tetromino

