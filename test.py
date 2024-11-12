import mcp2515
import random
import time

can = mcp2515.SPIController()

try:
    while True:
        print("RX: " + str(can.poll_receive()))
        can_id = int(random.random() * 0x7FF)
        print("TX: " + str(([can_id], [ord(c) for c in "owo"])))
        can.transmit(can_id, bytes("owo", "ASCII"))
        time.sleep(1)

except KeyboardInterrupt:
    can.spi.close()