import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

# Set params
plt.rcParams.update({'font.size': 22})
n = 30000

# make x-axis
x_axis = range(n)

# Read data
table = pd.read_csv("data/meanstdlog.csv")
x = table['mean']
y = table['std']

# Plot
plt.plot(x_axis, x, label = 'Mean L|LO')
plt.fill_between(x_axis,x-y, x+y, color = 'yellow', label = 'Std. L|LO', alpha = 0.3)

# Same process as above repeated.
table = pd.read_csv("data/meanstdlinnewtemp.csv")
x = table['mean']
y = table['std']
plt.plot(x_axis, x, label = 'Mean L|L')
plt.fill_between(x_axis,x-y, x+y, color = 'green', label = 'Std. L|L', alpha = 0.3)

config_1 = np.zeros((25, n))
# LB|LB
table = pd.read_csv("data/energy_LB_LB.csv", usecols=[0])
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config ==5:
        x = 1
    config_1[config][timestep] = float(value)

x  = config_1.mean(axis=0)
y = config_1.std(axis=0)

plt.plot(x_axis[0: len(x_axis) - 2], x[0:len(x) - 2], label = 'Mean LB|LB')
plt.fill_between(x_axis,x-y, x+y, label = 'Std. LB|LB', alpha = 0.3)
plt.grid()

# L|LB
config_2 = np.zeros((25, n))
table = pd.read_csv("data/energy_L_LB.csv", usecols=[0])


for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config ==5:
        x = 1
    config_2[config][timestep] = float(value)

x_2  = config_2.mean(axis=0)
y_2 = config_2.std(axis=0)
plt.plot(x_axis[0: len(x_axis) - 2], x_2[0:len(x_2) - 2], label = 'Mean L|LB')
plt.fill_between(x_axis,x_2-y_2, x_2+y_2, color = 'brown', label = 'Std. L|LB', alpha = 0.3)

#LB|L
table = pd.read_csv("data/energy_LB_L.csv", usecols=[0])
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config ==5:
        x = 1
    config_1[config][timestep] = float(value)

x  = config_1.mean(axis=0)
y = config_1.std(axis=0)

plt.plot(x_axis[0: len(x_axis) - 2], x[0:len(x) - 2], label = 'Mean LB|L')
plt.fill_between(x_axis,x-y, x+y, color = 'red', label = 'Std. LB|L', alpha = 0.3)

#LB|LO
table = pd.read_csv("data/energy_LB_LO.csv", usecols=[0])
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config ==5:
        x = 1
    config_1[config][timestep] = float(value)

x  = config_1.mean(axis=0)
y = config_1.std(axis=0)

plt.plot(x_axis[0: len(x_axis) - 2], x[0:len(x) - 2], label = 'Mean LB|LO')
plt.fill_between(x_axis,x-y, x+y, color = 'red', label = 'Std. LB|LO', alpha = 0.3)

plt.xlabel('iterations')
plt.ylabel('Energy [a.u.]')

plt.legend(loc = 'upper left')
plt.show()