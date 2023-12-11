import asyncio
import time
import math
import moteus
import numpy as np
import csv
import os

async def main():
    qr = moteus.QueryResolution()
    qr._extra =  {
        moteus.Register.MILLISECOND_COUNTER: moteus.F32,
        moteus.Register.Q_CURRENT: moteus.F32,
    }
    c = moteus.Controller(query_resolution=qr)
    await c.set_stop()

    motor = input('which motor? ')
    file_num = input('input trial number: ')
    filename = 'rail_climb_'+motor+'_'+ '_trial_'+file_num+ '.csv'
    folder_path = '/Users/adamhung/Desktop/embir/mod_leg/mod_leg/Experiments/Exp3'
    full_path = os.path.join(folder_path, filename)
 
    state = await c.set_position(position=math.nan, query=True)

    #variables for oscillation behavior
    angle = 1
    start = state.values[moteus.Register.POSITION]         
    end = start + angle    
    A = angle
    C = -math.pi/2
    D = A + start
    start_freq = 0.5
    num_steps  = 3
    cur_step = 0
    #end_freq = 0.8
    #f_inc = 1.2

    # open io stream for writing to csv file
    with open(full_path, mode='w') as csvfile:
        # format setup for csv file
        fieldnames = ['time', 'position', 'velocity', 'q_current', 'command_position']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # figure out command position based on frequency and various timers
        prog_start = time.perf_counter()
        wave_start = prog_start
        f = start_freq
        #while f <= end_freq:
        while cur_step < num_steps:
            time1 = time.perf_counter()
            t_plot = time1 - prog_start
            t_wave = time1 - wave_start
            B = 2*math.pi*f
            command_pos = A * math.sin(B*t_wave + C) + D   
            if t_wave >= 1/f:
                cur_step +=1
                wave_start = time.perf_counter()
                #f = f*f_inc
                #print('frequency: ', f)
            
            # command actuator to calculated position
            state = await c.set_position(position=command_pos, query=True)
            # read data from actuator register
            pos = state.values[moteus.Register.POSITION]
            v = state.values[moteus.Register.VELOCITY]
            i_q = state.values[moteus.Register.Q_CURRENT]
            # write to csv
            writer.writerow({'time': t_plot, 'position': pos, 'velocity': v, 'q_current': i_q, 'command_position': command_pos})
            # time delay
            delta = time.perf_counter() - time1
            if delta>0:
                await asyncio.sleep(0.0125 - delta)
            else:
                print("loop frequency exceeding 0.0125")

    # kill power to motor
    await c.set_stop()
    print("Done, wrote data to: ", filename)
    return

if __name__ == '__main__':
    asyncio.run(main())