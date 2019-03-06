from evdev import InputDevice, categorize, ecodes
from enum import Enum

class Direction(Enum):
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


class Instruction:
    def __init__(self, direction):
        self.direction = direction

    def send_instruction(self):
        pass

def resolve_absevent(abs_event):
    if abs_event.type == ecodes.EV_ABS:
        categorized = categorize(abs_event)
        type_code = ecodes.bytype[categorized.event.type][categorized.event.code]
        value = categorized.event.value
        #print(value)
        if type_code == "ABS_X":
            if value < 128:
                return Instruction(Direction.LEFT)
            elif value > 128:
                return Instruction(Direction.RIGHT)
        elif type_code == "ABS_Y":
            if value < -129:
                return Instruction(Direction.FORWARD)
            elif value > -129:
                return Instruction(Direction.BACKWARD)
        elif type_code == "ABS_RX":
            if value < 128:
                return Instruction(Direction.COUNTERCLOCKWISE)
            elif value > 128:
                return Instruction(Direction.CLOCKWISE)
        elif type_code == "ABS_RY":
            if value < -129:
                return Instruction(Direction.UP)
            elif value > -129:
                return Instruction(Direction.DOWN)
        return Instruction(Direction.NEUTRAL)
    return Instruction(Direction.UNKNOWN)

def resolve_btnevent(btn_event):
    if event.type == ecodes.EV_KEY:
        categorized = categorize(event)
        key = categorized.keycode
        key_state = categorized.keystate
        if key_state == 1:
            if "BTN_Y" in key:
                return Instruction(Direction.FORWARD)
            elif "BTN_A" in key:
                return Instruction(Direction.BACKWARD)
            elif "BTN_X" in key:
                return Instruction(Direction.LEFT)
            elif "BTN_B" in key:
                return Instruction(Direction.RIGHT)
        elif key_state == 0:
            return Instruction(Direction.NEUTRAL)
    return Instruction(Direction.UNKNOWN)


gamepad = InputDevice('/dev/input/event18')
previous_instruction = Instruction(Direction.NEUTRAL)
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        print(resolve_btnevent(event).direction)
    elif event.type == ecodes.EV_ABS:
        current_instruction = resolve_absevent(event)
        if current_instruction.direction == Direction.NEUTRAL:
            print(current_instruction.direction)
        if previous_instruction is not None and previous_instruction.direction != current_instruction.direction:
            if previous_instruction.direction == Direction.NEUTRAL:
                print(current_instruction.direction)
        previous_instruction = current_instruction

        