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
    filename = 'rail_climb_'+motor+'_'+ '_trial_'+trial_num+ '.csv'
    folder_path = '/Users/adamhung/Desktop/embir/mod_leg/mod_leg/Experiments/Exp3'
    full_path = os.path.join(folder_path, filename)
 
    state = await c.set_position(position=math.nan, query=True)

    #variables for movement
    angle = 0.8
    start = 0.5 + state.values[moteus.Register.POSITION]        
    end = start + angle
    poses = [start, end]
    num_steps  = 3
    eps = 0.2

    start_timer = time.perf_counter()
    while (time.perf_counter() - start_timer < 1):
        state = await c.set_position(position=start, query=True, velocity_limit = 15)
        print("going to start pos")
    
    
    # open io stream for writing to csv file
    with open(full_path, mode='w') as csvfile:
        # format setup for csv file
        fieldnames = ['time', 'position', 'velocity', 'q_current', 'command_position']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        prog_start = time.perf_counter()
        print("entering loop")

        for i in range(num_steps):
            print("hi")
            for pose in poses:
                print("hi2")
                # sends position command and logs data until within eps of target position
                while abs(state.values[moteus.Register.POSITION] - pose) > eps:
                    print("hi3")
                    state = await c.set_position(position=pose, query=True)

                    t = time.perf_counter() - prog_start
                    pos = state.values[moteus.Register.POSITION]
                    v = state.values[moteus.Register.VELOCITY]
                    i_q = state.values[moteus.Register.Q_CURRENT]
                    print('going to: ', pose, ', at: ', pos)

                    writer.writerow({'time': t, 'position': pos, 'velocity': v, 'q_current': i_q})

    # kill power to motor
    await c.set_stop()
    print("Done, wrote data to: ", filename, " at: ", full_path)
    return

if __name__ == '__main__':
    asyncio.run(main())