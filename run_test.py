import asyncio
import math
import moteus
import numpy as np

num_steps = 2
angle = 1.2 #1.375
angle = angle*15.0/3.1415/2

async def main():
    i = 0
    c = moteus.Controller()
    await c.set_stop()
    result = await c.set_position_wait_complete(position=0, accel_limit=2.0)
    print("stepping now")
    while i<num_steps:
        result = await c.set_position_wait_complete(position=angle, velocity_limit = 2)
        result = await c.set_position_wait_complete(position=0, velocity_limit = 2)
        i=i+1
        print("just stepped")


    await c.set_stop()
    print("done")


if __name__ == '__main__':
    asyncio.run(main())