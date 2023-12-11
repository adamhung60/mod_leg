import asyncio
import time
import math
import moteus
import numpy as np
import matplotlib.pyplot as plt


async def main():

    rise_times = []
    overshoots = []
    angle = 0.5

    for q in range(4):

        print('trial ', q)
        qr = moteus.QueryResolution()
        qr._extra =  {
            moteus.Register.MILLISECOND_COUNTER: moteus.F32,
            moteus.Register.Q_CURRENT: moteus.F32,
        }
        c = moteus.Controller(query_resolution=qr)
        await c.set_stop()
        state = await c.set_position(position=math.nan, query=True)
        start = state.values[moteus.Register.POSITION]         
        end = start + angle    
        current_pos = start
        times = []
        poses = []
        #currents = []
        prog_start = time.perf_counter()
        #while current_pos < end - 0.1:
        while (time.perf_counter() - prog_start) < 2:
            state = await c.set_position(position=end, query=True)
            t_plot = time.perf_counter() - prog_start
            # read data from actuator register
            current_pos = state.values[moteus.Register.POSITION]
            #i_q = state.values[moteus.Register.Q_CURRENT]
            times.append(t_plot)
            poses.append(current_pos)
            #currents.append(i_q)

        # kill power to motor
        await c.set_stop()

        ten_p = start + 0.1 * angle
        ninety_p = start + 0.9 * angle

        # Find indices corresponding to the desired position range
        middle_eighty_indices = [i for i, pos in enumerate(poses) if ten_p <= pos <= ninety_p]
        """plt.plot(times, poses, marker='o', linestyle='-',linewidth=1)
        plt.plot([times[i] for i in middle_eighty_indices], [poses[i] for i in middle_eighty_indices], marker='o', linestyle='-', color='red',linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Position')
        plt.title('Position vs Time')
        plt.show()"""

        """plt.plot(times, currents, marker='o', linestyle='-',linewidth=1)
        plt.xlabel('Time')
        plt.ylabel('current')
        plt.title('current vs Time')
        plt.show()"""

        rise_time = times[middle_eighty_indices[-1]] - times[middle_eighty_indices[0]]
        rise_times.append(rise_time)
        overshoot = max(poses)-end
        overshoots.append(overshoot)
        await asyncio.sleep(2)

    print('rise times: ' , rise_times)
    print('mean rise time: ' , np.mean(rise_times))
    print('mean percent overshoot: ', 100*(np.mean(overshoots))/angle)
    
    """plt.hist(rise_times, bins=10, edgecolor='black')
    plt.xlabel('Rise Times')
    plt.ylabel('Frequency')
    plt.title('Histogram of Rise Times')
    plt.show()"""


if __name__ == '__main__':
    asyncio.run(main())