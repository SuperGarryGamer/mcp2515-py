#!/usr/bin/python3
# Written by Jay 2024-11-05

import spidev

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

spi = None

def initialize():
    global spi
    spi = spidev.SpiDev()
    spi.max_speed_hz = SPI_FREQUENCY_HZ
    spi.mode = 0b00 # One of two modes supported by MCP2515, chosen arbitrarily because i don't know
    spi.open(0, SPI_DEVICE)

def reset():
    global spi
    spi.writebytes(0b11000000.to_bytes())