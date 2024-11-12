#!/usr/bin/python3
# Written by Jay 2024-11-05

import spidev
import time

# MCP2515 Register addresses

TXB0 = {
    "CTRL": 0b00110000,
    "SIDH": 0b00110001,
    "SIDL": 0b00110010,
    "EID8": 0b00110011,
    "EID0": 0b00110100,
    "DLC":  0b00110101,
    "D0":   0b00110110,
    "D1":   0b00110111,
    "D2":   0b00111000,
    "D3":   0b00111001,
    "D4":   0b00111010,
    "D5":   0b00111011,
    "D6":   0b00111100,
    "D7":   0b00111101,
}
TXB1 = {
    "CTRL": 0b01000000,
    "SIDH": 0b01000001,
    "SIDL": 0b01000010,
    "EID8": 0b01000011,
    "EID0": 0b01000100,
    "DLC":  0b01000101,
    "D0":   0b01000110,
    "D1":   0b01000111,
    "D2":   0b01001000,
    "D3":   0b01001001,
    "D4":   0b01001010,
    "D5":   0b01001011,
    "D6":   0b01001100,
    "D7":   0b01001101,
}
TXB2 = {
    "CTRL": 0b01010000,
    "SIDH": 0b01010001,
    "SIDL": 0b01010010,
    "EID8": 0b01010011,
    "EID0": 0b01010100,
    "DLC":  0b01010101,
    "D0":   0b01010110,
    "D1":   0b01010111,
    "D2":   0b01011000,
    "D3":   0b01011001,
    "D4":   0b01011010,
    "D5":   0b01011011,
    "D6":   0b01011100,
    "D7":   0b01011101,
}
RXB0 = {
    "CTRL": 0b01100000,
    "SIDH": 0b01100001,
    "SIDL": 0b01100010,
    "EID8": 0b01100011,
    "EID0": 0b01100100,
    "DLC":  0b01100101,
    "D0":   0b01100110,
    "D1":   0b01100111,
    "D2":   0b01101000,
    "D3":   0b01101001,
    "D4":   0b01101010,
    "D5":   0b01101011,
    "D6":   0b01101100,
    "D7":   0b01101101,
}
RXB1 = {
    "CTRL": 0b01110000,
    "SIDH": 0b01110001,
    "SIDL": 0b01110010,
    "EID8": 0b01110011,
    "EID0": 0b01110100,
    "DLC":  0b01110101,
    "D0":   0b01110110,
    "D1":   0b01110111,
    "D2":   0b01111000,
    "D3":   0b01111001,
    "D4":   0b01111010,
    "D5":   0b01111011,
    "D6":   0b01111100,
    "D7":   0b01111101,
}
# Use Raspberry Pi's SPI0 or SPI1
SPI_DEVICE = 0

# Max from the datasheet (10 MHz)
SPI_FREQUENCY_HZ = 10_000_000

class SPIController:

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_FREQUENCY_HZ
        self.spi.mode = 0b00 # One of two modes supported by MCP2515, chosen arbitrarily because i don't know
        self.reset()
        time.sleep(0.1)

    def reset(self):
        self.spi.writebytes(0b11000000.to_bytes())

    def transmit(self, can_id: int, message: bytes):
        # Sanity check, max 8 bytes per CAN frame
        if len(message) > 8:
            raise ValueError

        # Sanity check, standard CAN ID is 11 bits max (this breaks extended IDs)
        if (can_id > 0x7FF):
            raise ValueError

        can_id_hi = can_id >> 3
        can_id_lo = (can_id & 0b0000000000000111) << 5

        # Write data to TXB0
        self.spi.xfer2(0b01000000.to_bytes() + can_id_hi.to_bytes() + can_id_lo.to_bytes() + 0x00.to_bytes() * 2 + len(message).to_bytes() + message) # i hope this works

        # Request to send TXB0
        self.spi.xfer2(0b10000001.to_bytes())

    def poll_receive(self):
        filler = 0x00.to_bytes() * 13 # enough padding to receive full message
        instruction = 0b10010000.to_bytes() + filler

        result = self.spi.xfer2(instruction)
        can_id = result[0] << 8 + result[1]
        return (can_id, result[5:])