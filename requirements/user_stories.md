# Requirements

### Game Options

* Game options shall allow the user to setup the following options:

   * Playfield dimensions
   * Mode of control
   * Control keys

#### Playfield dimensions
* The user shall be able to set the number of columns anywhere between 3 and 13, [3, 13].
* The user shall be able to set the number of rows anywhere between 4 and 20, [4, 20].

#### Mode of control
* The user shall be able to choose between relative and absolute mode of control.

##### Relative mode of control
* In relative control mode the tetromino shall be mobed gradually either to the adjacent left or adjacent right column.
* In relative control mode the tetromino shall be rotated gradually 90 degrees clockwise or 90 degrees counter-clockwise.

##### Absolute mode of control
* In absolute control mode the tetromino can be moved directly to any available column.
* In absolute control mode the tetromino can be rotated directly to any of the four directions (north, east, south, west).

### Custom Levels
* As a user with basic programming knowledge I want to be able to set up and sequence customized levels to define the progress through a session of absolutis.
