import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))





def read_channel(pin):
    value = map_values(mcp.read_adc(pin))
    return value

def read_joystick(pin):
    value = joystick(mcp.read_adc(pin))
    return value

def read_quick(pin):
    mcp.read_adc(pin)


def get_values():
    values = [0]*3
    for i in range(3):
        values[i] = map_values(mcp.read_adc(i))
    return values


def map_values(sensor_val):
    neutral = 512.0
    new_range = 100.0
    time_range = 100000.0
    dir_mod = 1

    read_diff = neutral - sensor_val
    
    if abs(read_diff) < 50:
        return 0
    if read_diff < 0:
        dir_mod = (-1)

    read_diff = abs(read_diff)
    scaled_read = (1.0 - float(read_diff / 512)) * new_range

    time_val = scaled_read / time_range
    time_val = round(time_val, 5)

    if time_val < 0.000075:
        time_val = 0.000075
    time_val = time_val * dir_mod

    return time_val


def joystick(sensor_val):
    neutral = 512.0
    new_range = 4.0
    dir_mod = 1

    read_diff = neutral - sensor_val
    
    if abs(read_diff) < 60:
        return 1000
    if read_diff < 0:
        dir_mod = (-1)

    read_diff = abs(read_diff)
    scaled_read = (1.0 - float(read_diff / 512)) * new_range
    time_val = int(scaled_read * dir_mod)
    return time_val
