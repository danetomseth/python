import time
import stepper

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))




def read_values():
    print('Reading MCP3008 values, press Ctrl-C to quit...')
    # Print nice channel column headers.
    print('| {0:>4} | {1:>4} | {2:>4} |'.format(*range(3)))
    print('-' * 57)
    # Main program loop.
    while stepper.stop() == False:
        # Read all the ADC channel values in a list.
        values = [0]*3
        for i in range(3):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = map_values(mcp.read_adc(i))
        # Print the ADC values.
        print('| {0:>4} | {1:>4} | {2:>4} |'.format(*values))
        # Pause for half a second.
        time.sleep(0.2)



def read_channel(pin):
    value = map_values(mcp.read_adc(pin))
    return value


def get_values():
    values = [0]*3
    for i in range(3):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = map_values(mcp.read_adc(i))
    return values


def map_values(sensor_val):
    neutral = 512.0
    new_range = 100.0
    time_range = 100000.0
    dir_mod = 1

    read_diff = neutral - sensor_val
    if abs(read_diff) < 40:
        return 0
    if read_diff < 0:
        dir_mod = (-1)

    read_diff = abs(read_diff)
    scaled_read = (1.0 - float(read_diff / 512)) * new_range
    # scaled_read = round(scaled_read, 1)
    time_val = scaled_read / time_range
    time_val = round(time_val, 4)
    if time_val < 0.00005:
        time_val = 0.00005
    time_val = time_val * dir_mod
    # time_val = scaled_read / 10000.0
    # if time_val < 0:
    #     time_val = (time_range + time_val)
    # else:
        # time_val = (new_range - scaled_read) / 10000.0

    return time_val