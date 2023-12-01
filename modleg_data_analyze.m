data = table2array(readtable("/Users/adamhung/Desktop/embir/mod_leg/mod_leg/step_trial_0.csv"));

time = data(:, 1);
time = ((time - time(1, 1)))';
position = ((data(:, 2)))';
velocity = (data(:, 3))';
q_current = (data(:, 4))';
d_current = (data(:, 5))';

plot(time, velocity);
