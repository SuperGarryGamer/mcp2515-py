import spidev
import queue

SPEED = 10_000_000 # 10 MHz SPI

global spi

class Can_Frame:
    def __init__(self):
        self.sid = 0
        self.data = []

def initialize():
    global spi
    print(spi)
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = SPEED
    spi.mode = 0b00
    print(spi)

    reset()

    # Switch to normal mode
    spi.writebytes(bytes([0x02, 0x0f, 0x00]))


def transmit_frame(frame: Can_Frame):
    global spi
    print(spi)
    if len(frame.data) > 8:
        raise ValueError
    if frame.sid > 0x07ff:
        raise ValueError
    
    to_transmit = [0x40, frame.sid >> 3, (frame.sid & 0x07) << 5, 0x00, 0x00, len(frame.data)]

    for i in range(len(frame.data)):
        to_transmit.append(frame.data[i])

    spi.writebytes(bytes(to_transmit))
    spi.writebytes(bytes([0x81]))

def reset():
    global spi
    spi.writebytes(bytes([0xc0]))

# Testing:
initialize()
f1 = Can_Frame()
f1.sid = 1234
f1.data = [160, 7, 200, 7]
input()
transmit_frame(f1)
spi.close()