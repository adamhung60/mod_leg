import asyncio
import time
import math
import moteus
import numpy as np
import csv
import os
import matplotlib.pyplot as plt


async def main():

    rise_times_arr = []
    rise_times = []
    angle = 1.5 
    kp_scales = [0.1, 0.5, 0.75, 2.0, 5.0, 10.0, 15.0]

    

    for kp_sc in kp_scales:

        for i in range(5):

            print('trial ', i)
            c = moteus.Controller()
            await c.set_stop()
            state = await c.set_position(position=math.nan, query=True)
            
            start = state.values[moteus.Register.POSITION]         
            end = start + angle    
            current_pos = start

            times = []
            poses = []

            prog_start = time.perf_counter()
            while current_pos < end - 0.1:
                print(kp_sc)
                state = await c.set_position(position=end, query=True, kp_scale = kp_sc, kd_scale = 1)
                t_plot = time.perf_counter() - prog_start
                # read data from actuator register
                current_pos = state.values[moteus.Register.POSITION]
                times.append(t_plot)
                poses.append(current_pos)

            # kill power to motor
            await c.set_stop()

            ten_p = start + 0.1 * angle
            ninety_p = start + 0.9 * angle

            # indices corresponding to the desired position range
            middle_eighty_indices = [i for i, pos in enumerate(poses) if ten_p <= pos <= ninety_p]
            """plt.plot(times, poses, marker='o', linestyle='-',linewidth=1)
            plt.plot([times[i] for i in middle_eighty_indices], [poses[i] for i in middle_eighty_indices], marker='o', linestyle='-', color='red',linewidth=2)
            plt.xlabel('Time')
            plt.ylabel('Position')
            plt.title('Position vs Time')
            plt.show()"""

            rise_time = times[middle_eighty_indices[-1]] - times[middle_eighty_indices[0]]
            rise_times.append(rise_time)
            await asyncio.sleep(1)


        #print(rise_times)
        #print(np.mean(rise_times))
        rise_times_arr.append(np.mean(rise_times))
    
    i = 0
    for rt in rise_times_arr:
        print('kp = ', kp_scales[i], ', mean_rise_time = ' , rt)
        i+=1

    plt.plot(kp_scales, rise_times_arr, marker='o', linestyle='-',linewidth=1)
    plt.xlabel('kp')
    plt.ylabel('mean rise time')
    plt.title('kp vs rise time')
    plt.show()
    
if __name__ == '__main__':
    asyncio.run(main())