import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('active_oscillation_trial_0.csv')

# Plotting
plt.plot(df['time'], df['command_position'], label='Command Position')
plt.plot(df['time'], df['position'], label='Position')
plt.xlabel('Time')
plt.ylabel('Position')
plt.legend()
plt.title('Position and Command Position Over Time')
plt.show()



df['timesteps'] = df['time'].diff()

# Plotting histogram for timesteps
plt.hist(df['timesteps'].dropna(), bins=20) 
plt.xlabel('Timestep')
plt.ylabel('Frequency')
plt.title('Timesteps')
plt.show()

top_10_timesteps = df['timesteps'].nlargest(10)

print("Top 10 maximum values of timesteps:")
print(top_10_timesteps)