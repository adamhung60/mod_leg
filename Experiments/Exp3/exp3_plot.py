import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('rail_climb_trial_0.csv')

# Plotting
plt.plot(df['time'], df['command_position'], label='Command Position')
plt.plot(df['time'], df['position'], label='Position')
plt.xlabel('Time')
plt.ylabel('Position')
plt.legend()
plt.title('Position and Command Position Over Time')
plt.show()