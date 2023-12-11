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
        moteus.Register.D_CURRENT: moteus.F32
    }
    c = moteus.Controller(query_resolution=qr)
    await c.set_stop()

    file_num = input('input trial number: ')
    filename = 'n_steps_trial_'+file_num+ '.csv'

    num_steps = 3
    angle = 0.8*15.0/3.1415/2 #max 1.375
    eps = 0.1

    # set step endpoint angles based on the start position
    state = await c.set_position(position=math.nan, query=True)
    start_pos = state.values[moteus.Register.POSITION]
    print(start_pos)
    poses = [start_pos, start_pos - angle]

    # open io stream for writing to csv file
    with open(filename, mode='w') as csvfile:
        fieldnames = ['time', 'position', 'velocity', 'q_current', 'd_current']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(num_steps):
            for pose in poses:
                # sends position command and logs data until within eps of target position
                while abs(state.values[moteus.Register.POSITION] - pose) > eps:
                    state = await c.set_position(position=pose, query=True)
                    print("At:", state.values[moteus.Register.POSITION], "      Going to: ", pose)

                    t = state.values[moteus.Register.MILLISECOND_COUNTER] # ms since startup? wraps at 8388608
                    pos = state.values[moteus.Register.POSITION]
                    v = state.values[moteus.Register.VELOCITY]
                    i_q = state.values[moteus.Register.Q_CURRENT]
                    i_d = state.values[moteus.Register.D_CURRENT]

                    writer.writerow({'time': t, 'position': pos, 'velocity': v, 'q_current': i_q, 'd_current': i_d})
                
    # kill power to motor
    await c.set_stop()
    print("Done, wrote data to: ", filename)

if __name__ == '__main__':
    asyncio.run(main())






#python3 -m moteus.moteus_tool --target 1 --calibrate
#state = await c.set_position(position=pose,accel_limit=2.0,velocity_limit=2.0,query=True,)
#await asyncio.sleep(deltat)