from evdev import InputDevice, categorize, ecodes
from enum import Enum
import evdev
import serial

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

ser = serial.Serial("/dev/ttyACM0", 9600)

class Instruction:
    def __init__(self, direction):
        self.direction = direction

    def send_instruction(self):
        ser.write(b'%d'  % self.direction.value)

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


devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
device_path = ""
for device in devices:
    if "Gamepad" in device.name:
        device_path = device.path
        break

if device_path == "":
    print("Couldn't find the gamepad. Check the connection.")
else:
    print("Listening on: ", device_path)
    print("Sending to: ", "/dev/ttyACM0")
    gamepad = InputDevice(device_path)
    previous_instruction = Instruction(Direction.NEUTRAL)
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            instruction = resolve_btnevent(event)
            instruction.send_instruction()
            print(instruction.direction)
        elif event.type == ecodes.EV_ABS:
            current_instruction = resolve_absevent(event)
            if current_instruction.direction == Direction.NEUTRAL:
                current_instruction.send_instruction()
                print(current_instruction.direction)
            if previous_instruction is not None and previous_instruction.direction != current_instruction.direction:
                if previous_instruction.direction == Direction.NEUTRAL:
                    current_instruction.send_instruction()
                    print(current_instruction.direction)
            previous_instruction = current_instruction

        
