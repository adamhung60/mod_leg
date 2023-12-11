import asyncio
import math
import moteus
import numpy as np
import csv

async def main():
    qr = moteus.QueryResolution()
    qr._extra =  {
        moteus.Register.MILLISECOND_COUNTER: moteus.F32,
        moteus.Register.Q_CURRENT: moteus.F32,
    }
    c = moteus.Controller(query_resolution=qr)
    await c.set_stop()

    file_num = input('input trial number: ')
    filename = 'passive_drop_trial_'+file_num+ '.csv'

    # set step endpoint angles based on the start position
    state = await c.set_position(position=math.nan, query=True)

    # open io stream for writing to csv file
    with open(filename, mode='w') as csvfile:
        fieldnames = ['time', 'position', 'velocity', 'q_current', 'd_current']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        t = state.values[moteus.Register.MILLISECOND_COUNTER] # ms since startup? wraps at 8388608
        pos = state.values[moteus.Register.POSITION]
        v = state.values[moteus.Register.VELOCITY]
        i_q = state.values[moteus.Register.Q_CURRENT]

        writer.writerow({'time': t, 'position': pos, 'velocity': v, 'q_current': i_q, 'd_current': i_d})
                
    # kill power to motor
    await c.set_stop()
    print("Done, wrote data to: ", filename)

if __name__ == '__main__':
    asyncio.run(main())
