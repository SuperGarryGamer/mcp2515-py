import spidev
import sys
import signal
import RPi.GPIO as gpio
import queue

SPEED = 10_000_000 # 10 MHz SPI
INTERRUPT_PIN = 25 # GPIO25, 11th pin on the outside row (physical pin 22)

global spi

class Can_Frame:
    def __init__(self):
        self.sid = 0
        self.data = []

def initialize():
    global spi
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = SPEED
    spi.mode = 0b00
    print(spi)

    reset()

    # Switch to normal mode
    spi.writebytes(bytes([0x02, 0x0f, 0x00]))
    # Enable message receive interrupt for RXB0
    spi.writebytes(bytes([0x02, 0x2b, 0x01]))


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

def read_rxb0():
    global spi
    to_xfer = bytes([0x90] + [0x00]*13)
    recv = spi.xfer(to_xfer)
    new_frame = Can_Frame()
    new_frame.sid = recv[1] << 3
    new_frame.sid += (recv[2] >> 5)
    for i in range(recv[5]):
        new_frame.data.append(recv[6+i])
    return new_frame

def reset():
    global spi
    spi.writebytes(bytes([0xc0]))

def on_can_interrupt(channel):
    num_interrupts += 1
    print(f"I got an interrupt :3, {num_interrupts}")

# Testing:
initialize()
f1 = Can_Frame()
f1.sid = 1234
f1.data = [160, 7, 200, 7]
input()
transmit_frame(f1)

# Testing
gpio.setmode(gpio.BCM)
gpio.setup(INTERRUPT_PIN, gpio.IN)
gpio.add_event_detect(INTERRUPT_PIN, gpio.FALLING, callback=on_can_interrupt, bouncetime=50)

num_interrupts = 0

while num_interrupts < 5:
    pass

spi.close()