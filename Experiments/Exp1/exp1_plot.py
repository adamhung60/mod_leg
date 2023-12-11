import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('active_oscillation_1_trial_1.csv')


# plot cutoff
angle = 0.5
start = df['command_position'][0]        
end = start + 2*angle   
x_values = np.linspace(0, 22, 100)
y_values = (start + 1.7/2*(end - start)) * np.ones_like(x_values)
y_values_2 = (start + 1.3/2*(end - start)) * np.ones_like(x_values)
plt.plot(x_values, y_values, label='Cutoff Frequency', color='red')
plt.plot(x_values, y_values_2, label='30 percent amplitude', color='black')

# Plotting data
plt.plot(df['time'], df['command_position'], label='Command Position', color='blue')
plt.plot(df['time'], df['position'], label='Position', color='green')
plt.xlabel('Time')
plt.ylabel('Position')
plt.legend()
plt.title('Position and Command Position Over Time (R150)')
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