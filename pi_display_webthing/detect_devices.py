import smbus
from typing import List, Optional


def scan() -> List[str]:
    devices = []
    try:
        bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1
        for device in range(128):
            try:
                bus.read_byte(device)
                devices.append(hex(device))
            except:
                pass
    except FileNotFoundError as e:
        print("I2C seems not to be activated")
    return devices
