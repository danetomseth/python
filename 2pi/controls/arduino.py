import time 
import serial
import stepper

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    print("ARDUINO CONNECTED")
except:
    print("ARDUINO ERROR")


def first_item():
    ser.write('1x')
    # while stepper.stop() == False:
    #     message = ser.readline()
    #     print(message)
    print("DONE")

def second_item(speed):
    print("SPEED: " + speed)
    ser.write(speed)
    # while stepper.stop() == False:
    #     message = ser.readline()
    #     print(message)
    print("DONE")

def slide():
    ser.write('s')
    # print(ser.read())
    ser.write('100/')
    while stepper.stop() == False:
        pass
    # ser.reset_input_buffer()
    ser.write('x')
    print(ser.read(10))


def pan():
    ser.write('p')
    print(ser.read())
    ser.write('100/')
    while stepper.stop() == False:
        pass
    ser.write('x')
    print(ser.read())

def tilt():
    ser.write('t')
    print(ser.read())
    ser.write('100/')
    while stepper.stop() == False:
        pass
    ser.write('x')
    print(ser.read())


def fast():
    ser.write("20x")
def stop():
    ser.write('0x')