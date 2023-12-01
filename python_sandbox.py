import numpy as np
import time
import math
import matplotlib.pyplot as plt  


angle = 1.9
start = 0.5   
end = start + angle    

poses = []
times = []
A = end - start
C = -math.pi/2
D = start

wave_start = time.perf_counter()
prog_start = wave_start

f = 0.1
while f <= 1:
    t_plot = time.perf_counter() - prog_start
    t = time.perf_counter() - wave_start
    B = 2*math.pi*f
    command_pos = A * math.sin(B*t + C) + D   
    times.append(t_plot)
    poses.append(command_pos)  
    if t >= 1/f:
        wave_start = prog_start + t_plot
        f += 0.05


plt.plot(times, poses)
plt.title("poses by time")
plt.xlabel("Time")
plt.ylabel("poses")
plt.grid(True)
plt.show()