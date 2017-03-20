import time 
import serial
import stepper

ser = serial.Serial('/dev/ttyACM0', 9600)


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

def fast():
    ser.write("20x")
def stop():
    ser.write('0x')