import numpy as np
import matplotlib.pyplot as plt

# Assuming your data is stored in a file named 'data.txt'
#with open('force_plate/drop2.3.1.txt', 'r') as file:
with open('/Users/adamhung/Desktop/embir/mod_leg/res_test.txt', 'r') as file:
    # Read lines from the file
    lines = file.readlines()

# Extract the Fz column values
time_values = []
fz_values = []

for line in lines[3:]:  # Skip the first three lines with headers and units
    values = [float(val) for val in line.split(',')]
    time_values.append(values[0])  # Assuming time values are in the first column
    fz_values.append(values[2])   # Assuming Fz values are in the third column

# Calculate time in seconds based on the given rate (500 Hz)
time_seconds = np.arange(0, len(time_values) / 500, 1 / 500)

start_index = int(3.75 * 500)
end_index = int(4.25 * 500)

# Plot Fz values within the specified time range
plt.plot(time_seconds[start_index:end_index], fz_values[start_index:end_index])
#plt.plot(time_seconds, fz_values)
plt.xlabel('Time (seconds)')
plt.ylabel('Fz Values (N)')
#plt.title('Fz Values vs. Time (t = 10 to 20 seconds)')
plt.grid(True)
plt.show()


