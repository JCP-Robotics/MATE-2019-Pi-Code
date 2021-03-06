from evdev import InputDevice, categorize, ecodes
from enum import Enum
from nanpy import SerialManager, ArduinoApi
import evdev
import serial
import nanpy
from instructionsender import InstructionSender, ServoSender
import instructionsender

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

# search for connected Arduino and try to connect to it
arduino_conn = None
try:
    arduino_conn = SerialManager()
    arduino_conn.open()
except:
    print("Couldn't find the Arduino. Check the connection.")

arduino_api = None
if arduino_conn is not None:
    arduino_api = ArduinoApi(connection=arduino_conn)

if arduino_api is not None:
    sender = InstructionSender(arduino_api)
    sender.setup()

if arduino_api is not None:
    servosender = ServoSender()
    servosender.stop()

class Instruction:
    def __init__(self, direction, prev=None, instruction2=None, source=""):
        self.direction = direction
        self.prev = prev
        self.source = source
        self.instruction2 = instruction2

    def send_instruction(self):
        #fwd = counterclockwise
        if sender is not None:
            if self.direction == Direction.UP:
                servosender.spin_reverse(400)
            elif self.direction == Direction.DOWN:
                servosender.spin_forward(400)
            elif self.direction == Direction.FORWARD:
                sender.forward()
            elif self.direction == Direction.BACKWARD:
                sender.backward()
            elif self.direction == Direction.LEFT:
                sender.left()
            elif self.direction == Direction.RIGHT:
                sender.right()
            elif self.direction == Direction.UNKNOWN:
                pass
            elif self.direction == Direction.NEUTRALR:
                servosender.stop()
                '''if self.prev is not None:
                    if self.prev == Direction.UP or self.prev == Direction.DOWN:
                        servosender.stop()
                        print("stop")
                    else:
                        sender.stopall()'''
            elif self.direction == Direction.NEUTRALL:
                sender.stopall()
            elif self.direction == Direction.NEUTRAL:
                servosender.stop()
                sender.stopall()
            elif self.direction == Direction.CLOCKWISE:
                sender.clockwise()
            elif self.direction == Direction.COUNTERCLOCKWISE:
                sender.counterclockwise()

def resolve_absevent(abs_event):
    if abs_event.type == ecodes.EV_ABS:
        categorized = categorize(abs_event)
        type_code = ecodes.bytype[categorized.event.type][categorized.event.code]
        value = categorized.event.value
        #print(value)
        if type_code == "ABS_X":
            if value < 128:
                return Instruction(Direction.LEFT, source="left")
            elif value > 128:
                return Instruction(Direction.RIGHT, source="left")
            else:
                return Instruction(Direction.NEUTRALL, source="left")
        elif type_code == "ABS_Y":
            if value < -129:
                return Instruction(Direction.FORWARD, source="left")
            elif value > -129:
                return Instruction(Direction.BACKWARD, source="left")
            else:
                return Instruction(Direction.NEUTRALL, source="left")
        elif type_code == "ABS_RX":
            if value < 128:
                return Instruction(Direction.COUNTERCLOCKWISE, source="right")
            elif value > 128:
                return Instruction(Direction.CLOCKWISE, source="right")
            else:
                return Instruction(Direction.NEUTRALR, source="right")
        elif type_code == "ABS_RY":
            if value < -129:
                return Instruction(Direction.UP, source="right")
            elif value > -129:
                return Instruction(Direction.DOWN, source="right")
            else:
                return Instruction(Direction.NEUTRALR, source="right")
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

# search for connected game controller
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
            # if the current instrucion is sent from left joystick
            if current_instruction.source == "left":
                # handle the neutral position
                if current_instruction.direction == Direction.NEUTRALL:
                    # save the instruction from right joystick and send the current instruction
                    current_instruction.instruction2 = previous_instruction[1]
                    current_instruction.send_instruction()
                    print(current_instruction.direction)
                # check if the previous instruction is the same as the current instruction
                if previous_instruction is not None and previous_instruction[0].direction != current_instruction.direction:
                    # handle the instruction only if previous instruction is neutral
                    if previous_instruction[0].direction == Direction.NEUTRALL:
                        current_instruction.instruction2 = previous_instruction[1]
                        current_instruction.send_instruction()
                        print(current_instruction.direction)
                # update previous instruction
                previous_instruction[0] = current_instruction
            # if the current instruction is sent from right joystick
            if current_instruction.source == "right":
                if current_instruction.direction == Direction.NEUTRALR:
                    current_instruction.instruction2 = previous_instruction[0]
                    current_instruction.send_instruction()
                    print(current_instruction.direction)
                if previous_instruction is not None and previous_instruction[1].direction != current_instruction.direction:
                    if previous_instruction[1].direction == Direction.NEUTRALR:
                        current_instruction.instruction2 = previous_instruction[0]
                        current_instruction.send_instruction()
                        print(current_instruction.direction)
                previous_instruction[1] = current_instruction
                    
            '''if previous_instruction is not None and previous_instruction.direction != current_instruction.direction:
                if previous_instruction.direction == Direction.NEUTRAL:
                    current_instruction.send_instruction()
                    print(current_instruction.direction)
            previous_instruction = current_instruction'''

        
