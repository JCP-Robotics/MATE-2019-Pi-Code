# MATE-2019-Pi-Code
The code to run on the Raspberry Pi for our MATE Ranger 2019 robot.

## Instruction cheatsheet
Right now we are actually sending the instruction encoded as a single-byte character to the Arduino through serial. Each number is corresponding to a specified instruction which we are going to implement on the Arduino.

```
FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3
CLOCKWISE = 4
COUNTERCLOCKWISE = 5
UP = 6
DOWN = 7
NEUTRAL = 8
UNKNOWN = 9
```
