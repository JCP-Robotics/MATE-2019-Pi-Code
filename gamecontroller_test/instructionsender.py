from nanpy import SerialManager, ArduinoApi, Servo
import time

motor1Speed=2
motor2Speed=3
motor3Speed=4
motor4Speed=5
motor5Speed=6

motor1A=23
motor1B=25

motor2A=27
motor2B=29

motor3A=31
motor3B=33

motor4A=35
motor4B=37

motor5A=39
motor5B=41

servoPin = 8
centerTrottle = 1500

class InstructionSender:
    def __init__(self, api=None):
        self.api = api
        #self.servosender = ServoSender()
    
    def setup(self):
        if self.api is not None:
            self.api.pinMode(motor2Speed, self.api.OUTPUT)
            self.api.pinMode(motor3Speed, self.api.OUTPUT)
            self.api.pinMode(motor4Speed, self.api.OUTPUT)
            self.api.pinMode(motor5Speed, self.api.OUTPUT)
            self.api.pinMode(motor1A, self.api.OUTPUT)
            self.api.pinMode(motor1B, self.api.OUTPUT)
            self.api.pinMode(motor2A, self.api.OUTPUT)
            self.api.pinMode(motor2B, self.api.OUTPUT)
            self.api.pinMode(motor3A, self.api.OUTPUT)
            self.api.pinMode(motor3B, self.api.OUTPUT)
            self.api.pinMode(motor4A, self.api.OUTPUT)
            self.api.pinMode(motor4B, self.api.OUTPUT)
            self.api.pinMode(motor5A, self.api.OUTPUT)
            self.api.pinMode(motor5B, self.api.OUTPUT)
            
    def spin_forward(self, speed, speedPin, pinA, pinB):
        if self.api is not None:
            self.api.analogWrite(speedPin, speed)
            self.api.digitalWrite(pinA, self.api.HIGH)
            self.api.digitalWrite(pinB, self.api.LOW)
            
    def spin_reverse(self, speed, speedPin, pinA, pinB):
        if self.api is not None:
            self.api.analogWrite(speedPin, speed)
            self.api.digitalWrite(pinA, self.api.LOW)
            self.api.digitalWrite(pinB, self.api.HIGH)

    def stop(self, speedPin, pinA, pinB):
        if self.api is not None:
            self.api.analogWrite(speedPin, 0)
            self.api.digitalWrite(pinA, self.api.LOW)
            self.api.digitalWrite(pinB, self.api.LOW)
            
    def test(self):
        self.spin_reverse(255, motor1Speed, motor1A, motor1B)
        '''if self.servosender is not None:
            self.servosender.spin_forward(200)'''
        #time.sleep(5)
        #self.stop(motor1Speed, motor1A, motor1B)
        
class ServoSender:
    def __init__(self):
        self.servo = Servo(servoPin)
        self.servo.writeMicroseconds(centerTrottle)
        
    def spin_forward(self, speed):
        if self.servo is not None:
            self.stop()
            self.servo.writeMicroseconds(centerTrottle + speed)
            
    def spin_reverse(self, speed):
        if self.servo is not None:
            self.stop()
            self.servo.writeMicroseconds(centerTrottle - speed)
            
    def stop(self):
        if self.servo is not None:
            self.servo.writeMicroseconds(centerTrottle)
            
    def finalize(self):
        if self.servo is not None:
            self.servo.detach()
        
        