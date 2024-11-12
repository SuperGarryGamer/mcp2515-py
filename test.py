import mcp2515 as can
import random
import time

can.initialize()

try:
    while True:
        print(can.poll_receive())
        can.transmit(int(random.random() * 0x7FF), bytes("owo", "ASCII"))
        time.sleep(1)

except KeyboardInterrupt:
    can.spi.close()