import asyncio
import time
import math
import moteus
import numpy as np
import csv
import os
import matplotlib.pyplot as plt


async def main():
    c = moteus.Controller()
    await c.set_stop()
    state = await c.set_position(position=math.nan, query=True)

    #variables for oscillation behavior
    angle = 1.5
    angle = 3
    start = state.values[moteus.Register.POSITION]         
    end = start + angle    
    current_pos = start
    times = []
    poses = []

    prog_start = time.perf_counter()

    while abs(end - current_pos) > 0.1:
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
    plt.plot(times, poses, marker='o', linestyle='-',linewidth=1)
    plt.plot([times[i] for i in middle_eighty_indices], [poses[i] for i in middle_eighty_indices], marker='o', linestyle='-', color='red',linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.title('Position vs Time')
    plt.show()

    print('Rise time: ', times[middle_eighty_indices[-1]] - times[middle_eighty_indices[0]])


if __name__ == '__main__':
    asyncio.run(main())