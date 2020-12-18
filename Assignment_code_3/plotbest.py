import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# File plots the best solution for the different methods

plt.rcParams.update({'font.size': 18})
n = 30000
x_axis = range(n)
best_lin = 1000
best_log = 1000

for i in range(25):
    table = pd.read_csv("data/linsim" + str(i) + "newenergy.csv")
    vals = table['energies']
    if vals.iloc[-1] < best_lin:
        best_lin = vals.iloc[-1]
        best_linvals = vals

for i in range(25):
    table = pd.read_csv("data/logsim" + str(i) + ".csv")
    vals = table['energies']
    x = vals.iloc[-1]
    if vals.iloc[-1] < best_log:
        best_log = vals.iloc[-1]
        best_logvals = vals

# LB LB
table = pd.read_csv("data/energy_LB_LB.csv", usecols=[0])

index = 0
min_val = 1000
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config == 1:
        x = 1
    if float(value) < min_val:
        index = config

best_ls = table.iloc[:,0][n * index: n * index + n + 2]
p =best_ls.size
plt.plot(x_axis[1:], best_ls, label = 'Best LB|LB')

# L LB
table = pd.read_csv("data/energy_L_LB.csv", usecols=[0])

index = 0
min_val = 1000
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config == 1:
        x = 1
    if float(value) < min_val:
        index = config

best_ls = table.iloc[:,0][n * index: n * index + n + 2]
p =best_ls.size

plt.plot(x_axis[1:], best_ls, label = 'Best L|LB')

# LB L
table = pd.read_csv("data/energy_LB_L.csv", usecols=[0])

index = 0
min_val = 1000
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config == 1:
        x = 1
    if float(value) < min_val:
        index = config

best_ls = table.iloc[:,0][n * index: n * index + n + 2]
p =best_ls.size

plt.plot(x_axis[1:], best_ls, label = 'Best LB|L')


# LB LO
table = pd.read_csv("data/energy_LB_LO.csv", usecols=[0])

index = 0
min_val = 1000
for i, value in enumerate(table.iloc[:,0]):
    timestep = i % n
    config = int(i / n)
    if config == 1:
        x = 1
    if float(value) < min_val:
        index = config

best_ls = table.iloc[:,0][n * index: n * index + n + 2]
p =best_ls.size

plt.plot(x_axis[1:], best_ls, label = 'Best LB|LO')

plt.plot(x_axis, best_logvals, label = 'Best L|LO')
plt.plot(x_axis, best_linvals, label = 'Best L|L')
plt.grid()
plt.legend()
plt.show()