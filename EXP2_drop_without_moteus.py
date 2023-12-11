import asyncio
import time
import moteus
import csv
import os

async def main():
    c = moteus.Controller()
    await c.set_stop()

    motor = input('which motor? ')
    trial_num = input('input trial number: ')
    filename = 'drop_without_moteus_' + motor + '_trial_'+trial_num+ '.csv'
    folder_path = '/Users/adamhung/Desktop/embir/mod_leg/mod_leg/Experiments/Exp2'
    full_path = os.path.join(folder_path, filename)

    # open io stream for writing to csv file
    
    with open(full_path, mode='w') as csvfile:
        # format setup for csv file
        fieldnames = ['time', 'position', 'velocity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # get state
        state = await c.set_position(query=True)
        # read position data from actuator register
        start_pos = state.values[moteus.Register.POSITION]
        
        # waits for useful data to begin
        while True:
            state = await c.set_position(query=True)
            pos = state.values[moteus.Register.POSITION]
            if abs(pos - start_pos) > 0.01:
                prog_start = time.perf_counter()
                print("useful data starting!")
                break

        # records useful data
        while True:
            # get time
            t_plot = time.perf_counter() - prog_start
            # get the state
            state = await c.set_position(query=True)
            # read position data from actuator register
            pos = state.values[moteus.Register.POSITION]
            v = state.values[moteus.Register.VELOCITY]
            # write to csv
            writer.writerow({'time': t_plot, 'position': pos, 'velocity': v})
            # short time delay
            await asyncio.sleep(0.02)

if __name__ == '__main__':
    asyncio.run(main())