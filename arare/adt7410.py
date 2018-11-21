#coding: utf-8
import smbus

class ADT7410(object):
    bus_number = 1
    i2c_address = None

    def __init__(self, bus_number=1, i2c_address=0x48):
        self.bus_number = bus_number
        self.i2c_address = i2c_address

    def getTemp(self, degrees=True):
        tmp = self._getTemp()

        if not degrees:
            tmp = tmp * 1.8 + 32

        return tmp

    def _getTemp(self):
        bus = smbus.SMBus(self.bus_number)
        block = bus.read_i2c_block_data(self.i2c_address, 0x00, 12)

        tmp = (block[0] << 8 | block[1]) >> 3
        if(tmp >= 4096):
            tmp -= 8192
        tmp = tmp / 16.0

        return tmp

if __name__ == '__main__':
    a = ADT7410()
    print(a.getTemp())
