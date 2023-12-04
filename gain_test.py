import asyncio
import time
import math
import moteus
import numpy as np
import csv
import os
import matplotlib.pyplot as plt


async def main():

    rise_times = []

    for i in range(5):

        print('trial ', i)
        c = moteus.Controller()
        await c.set_stop()
        state = await c.set_position(position=math.nan, query=True)
        angle = 1.5
        start = state.values[moteus.Register.POSITION]         
        end = start + angle    
        print('start: ', start, ', end: ', end)
        current_pos = start
        times = []
        poses = []
        prog_start = time.perf_counter()
        while current_pos < end:
            state = await c.set_position(position=end, query=True)
            t_plot = time.perf_counter() - prog_start
            # read data from actuator register
            current_pos = state.values[moteus.Register.POSITION]
            times.append(t_plot)
            poses.append(current_pos)

        # kill power to motor
        await c.set_stop()

        ten_p = start + 0.1 * (end - start)
        ninety_p = start + 0.9 * (end - start)

        # Find indices corresponding to the desired position range
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

    print(rise_times)
    print(np.mean(rise_times))
    
    """plt.hist(rise_times, bins=10, edgecolor='black')

    plt.xlabel('Rise Times')
    plt.ylabel('Frequency')
    plt.title('Histogram of Rise Times')
    plt.show()"""


if __name__ == '__main__':
    asyncio.run(main())