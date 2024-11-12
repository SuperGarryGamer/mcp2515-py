import mcp2515 as can
import random
import time

can.initialize()

try:
    while True:
        print("RX: " + can.poll_receive())
        can_id = int(random.random() * 0x7FF)
        print("TX: " + [can_id] + [ord(c) for c in "owo"])
        can.transmit(can_id, bytes("owo", "ASCII"))
        time.sleep(1)

except KeyboardInterrupt:
    can.spi.close()