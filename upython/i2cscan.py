"""
This is helper script
helpful if you want to see if your i2c bus is working correct
"""

import machine
import utime

i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15), freq=400000)
machine.Pin(18).value(1)
utime.sleep(2)
while True:

    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:', len(devices))

    for device in devices:
        print("Decimal address: ", device, " | Hexa address: ", hex(device))
    utime.sleep(0.5)
