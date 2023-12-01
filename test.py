import asyncio
import math
import moteus

async def main():
    # default id 1, picks an arbitrary CAN-FD transport, prefering an attached fdcanusb.
    c = moteus.Controller()
    await c.set_stop()
    while True:
        state = await c.set_position(position=math.nan, query=True)
        print(state)
        print("Position:", state.values[moteus.Register.POSITION])
        print()

        # must be <= .1
        await asyncio.sleep(0.02)

if __name__ == '__main__':
    asyncio.run(main())