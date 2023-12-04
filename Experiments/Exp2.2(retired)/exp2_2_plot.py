import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('leg_drop_moteus_connected_trial_0.csv')

# Plotting
plt.plot(df['time'], df['position'], label='Position')
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Position Over Time')
plt.show()


