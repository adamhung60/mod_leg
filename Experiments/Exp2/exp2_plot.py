import numpy as np
import matplotlib.pyplot as plt

# Assuming your data is stored in a file named 'data.txt'
#with open('force_plate/drop2.3.1.txt', 'r') as file:
with open('/Users/adamhung/Desktop/embir/mod_leg/mod_leg/Experiments/Exp2/force_plate/drop2.2.1.txt', 'r') as file:
    # Read lines from the file
    lines = file.readlines()

# Extract the Fz column values
fz_values = []

for line in lines[3:]:  # Skip the first three lines with headers and units
    values = [float(val) for val in line.split(',')]
    fz_values.append(values[2])   # Assuming Fz values are in the third column

# Calculate time in seconds based on the given rate (500 Hz)
times = np.arange(0, len(fz_values) / 500.0, 1.0 / 500)

integral_values = np.cumsum(fz_values[:-1]) * np.diff(times)

# Plot the result

start_index = int(10 * 500)
end_index = int(15 * 500)

# Plot Fz values within the specified time range
plt.plot(times[start_index:end_index], fz_values[start_index:end_index])
#plt.plot(time_seconds, fz_values)
plt.xlabel('Time (seconds)')
plt.ylabel('Force (N)')
#plt.title('Fz Values vs. Time (t = 10 to 20 seconds)')
plt.grid(True)
plt.show()


