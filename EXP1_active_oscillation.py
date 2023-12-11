import asyncio
import time
import math
import moteus
import csv
import os

async def main():
    qr = moteus.QueryResolution()
    qr._extra =  {
        moteus.Register.Q_CURRENT: moteus.F32,
    }
    c = moteus.Controller(query_resolution=qr)
    await c.set_stop()

    motor = input('which motor? ')
    trial_num = input('input trial number: ')
    filename = 'active_oscillation_'+motor+ '_trial_'+trial_num+ '.csv'
    folder_path = '/Users/adamhung/Desktop/embir/mod_leg/mod_leg/Experiments/Exp1'
    full_path = os.path.join(folder_path, filename)
 
    state = await c.set_position(position=math.nan, query=True)

    #variables for oscillation behavior
    angle = 0.5
    start = state.values[moteus.Register.POSITION] + 0.8          
    A = angle
    C = -math.pi/2
    D = A + start
    start_freq = 1
    end_freq = 10
    steps_per_f = 4
    f_inc = 1.2

    start_timer = time.perf_counter()
    while (time.perf_counter() - start_timer < 1):
        state = await c.set_position(position=start, query=True, velocity_limit = 10)
        

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
        while f <= end_freq:
            time1 = time.perf_counter()
            t_plot = time1 - prog_start
            t_wave = time1 - wave_start
            B = 2*math.pi*f
            command_pos = A * math.sin(B*t_wave + C) + D   
            if t_wave >= steps_per_f/f:
                wave_start = time.perf_counter()
                f = f*f_inc
                print('frequency: ', f)
            
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







    