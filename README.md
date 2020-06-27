# Absolutris

Absolutris is the pygame frontend for the _absolon_ tetris engine. It is called Absolutris because its controls do not rotate or move the pieces relatively, but absolutely. There are four rotation keys, each to rotate a tetromino to face in one of the four directions. Similarly, there are ten movement keys to move the tetromino into one of the ten columns.

# Absolon

Absolon is a tetris engine developed primarily for competitive multiplayer, analytic replay, and machine learning. While its game mechanics are imitating the 1989 Nintendo version of Tetris by default, many parameters can be changed.

Absolon is structured as follows

```
+-----------------------------------------------+
|                                  +-------- +  |
|  +--------+      +--------+      | Random  |  |
|  | Mapper |<-----| Bagger |<---->| Numbers |  |
|  +--------+      +--------+      | Source  |  |
|      |                           +---------+  |
+------|----------------------------------------+
       |
       v
+-----------+
| Playfield |
+-----------+
```
