from evdev import InputDevice, categorize, ecodes
from enum import Enum
from nanpy import SerialManager, ArduinoApi
import evdev
import serial
import nanpy
from instructionsender import InstructionSender, ServoSender
import instructionsender
import time

'''from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice("/dev/input/event2")
for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        categorized = categorize(event)
        type_code = ecodes.bytype[categorized.event.type][categorized.event.code]
        value = categorized.event.value
        print(type_code, value)'''

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

#sender.stopall()
while(True):
    sender.forward()
    print("test")
    time.sleep(5)
    sender.stopall()
    time.sleep(5)

        
        