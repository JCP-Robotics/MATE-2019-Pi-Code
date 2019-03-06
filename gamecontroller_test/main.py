from evdev import InputDevice, categorize, ecodes
from enum import Enum
from nanpy import SerialManager, ArduinoApi
import evdev
import serial
import nanpy

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
    NEUTRALL = 10
    NEUTRALR = 11

arduino_conn = None
try:
    arduino_conn = SerialManager()
    arduino_conn.open()
except:
    print("Couldn't find the Arduino. Check the connection.")

arduino_api = None
if arduino_conn is not None:
    arduino_api = ArduinoApi(connection=arduino_conn)

class Instruction:
    def __init__(self, direction, source=""):
        self.direction = direction
        self.source = source;

    def send_instruction(self):
        pass
        #ser.write(b'%d'  % self.direction.value)

def resolve_absevent(abs_event):
    if abs_event.type == ecodes.EV_ABS:
        categorized = categorize(abs_event)
        type_code = ecodes.bytype[categorized.event.type][categorized.event.code]
        value = categorized.event.value
        #print(value)
        if type_code == "ABS_X":
            if value < 128:
                return Instruction(Direction.LEFT, "left")
            elif value > 128:
                return Instruction(Direction.RIGHT, "left")
            else:
                return Instruction(Direction.NEUTRALL, "left")
        elif type_code == "ABS_Y":
            if value < -129:
                return Instruction(Direction.FORWARD, "left")
            elif value > -129:
                return Instruction(Direction.BACKWARD, "left")
            else:
                return Instruction(Direction.NEUTRALL, "left")
        elif type_code == "ABS_RX":
            if value < 128:
                return Instruction(Direction.COUNTERCLOCKWISE, "right")
            elif value > 128:
                return Instruction(Direction.CLOCKWISE, "right")
            else:
                return Instruction(Direction.NEUTRALR, "right")
        elif type_code == "ABS_RY":
            if value < -129:
                return Instruction(Direction.UP, "right")
            elif value > -129:
                return Instruction(Direction.DOWN, "right")
            else:
                return Instruction(Direction.NEUTRALR, "right")
        #return Instruction(Direction.NEUTRAL)
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
    print("Sending to: ", arduino_conn.device)
    gamepad = InputDevice(device_path)
    previous_instruction = [Instruction(Direction.NEUTRALL, "left"), Instruction(Direction.NEUTRALR, "right")]
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            instruction = resolve_btnevent(event)
            instruction.send_instruction()
            print(instruction.direction)
        elif event.type == ecodes.EV_ABS:
            current_instruction = resolve_absevent(event)
            
            if current_instruction.source == "left":
                if current_instruction.direction == Direction.NEUTRALL:
                    print(current_instruction.direction)
                    current_instruction.send_instruction()
                if previous_instruction is not None and previous_instruction[0].direction != current_instruction.direction:
                    if previous_instruction[0].direction == Direction.NEUTRALL:
                        print(current_instruction.direction)
                        current_instruction.send_instruction()
                previous_instruction[0] = current_instruction
            
            if current_instruction.source == "right":
                if current_instruction.direction == Direction.NEUTRALR:
                    print(current_instruction.direction)
                    current_instruction.send_instruction()
                if previous_instruction is not None and previous_instruction[1].direction != current_instruction.direction:
                    if previous_instruction[1].direction == Direction.NEUTRALR:
                        print(current_instruction.direction)
                        current_instruction.send_instruction()
                previous_instruction[1] = current_instruction
                    
            '''if previous_instruction is not None and previous_instruction.direction != current_instruction.direction:
                if previous_instruction.direction == Direction.NEUTRAL:
                    current_instruction.send_instruction()
                    print(current_instruction.direction)
            previous_instruction = current_instruction'''

        
