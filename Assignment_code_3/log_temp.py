import numpy as np
import numba
from numba import njit
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd

TAU = np.sqrt(0.0001)
blocks = 24

N = 30000
T = np.zeros((N, 1))
n = 12
E = np.zeros((N, 1))
c = 0.5
d = 0.2
runs = 25
config = np.zeros((2*n + 1,2))
accept = np.zeros(N)
energies = np.zeros((runs, N))

@njit
def accept_reject(config, i, energies):
    '''Determines if next configuration is accepted'''
    dE = config[2*n][1] - config[2*n][0]
    
    if dE < 0:
        config[:n] = config[n:2*n] + 0
        config[2 * n][0] = config[2 * n][1] + 0
    else:
        U = np.random.rand()
        x = np.exp(-dE/T[i])
        if U < x:
            config[:n] = config[n:2*n] + 0
            config[2 * n][0] = config[2 * n][1] + 0
    energies[i] = config[2*n][0] + 0

@njit 
def move(config, iteration, energies):
    '''Update configuration'''
    inside = 0
 
    for i in range(n):
        x = TAU * np.random.randn()
        y = TAU * np.random.randn()
        x = x + config[i][0]
        y = y + config[i][1]
        if x**2 + y**2 <= 1.0:
            config[i + n][0] = x
            config[i + n][1] = y
            energy = 0
            for charge_i in config[n:2*n]:
                for charge_j in config[n:2*n]:
                    if charge_i[0] != charge_j[0]:
                        distance = np.sqrt(np.sum(np.square(charge_i - charge_j)))
                        energy += 1/distance
            config[2*n][1] = energy/2
            accept_reject(config, iteration, energies)


def sim(energies):
    '''Performs simulation'''
    for point_charge in range(2 * n):
        angle = 2 * np.pi * np.random.rand()
        radius = np.random.rand()
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        config[point_charge][0] = x
        config[point_charge][1] = y

    energy = 0
    for charge_i in config[0:n]:
        for charge_j in config[0:n]:
            if charge_i[0] != charge_j[0]:
                distance = np.sqrt(np.sum(np.square(charge_i - charge_j)))
                energy += 1/distance
    config[2 * n][0] = energy/2


    for i in numba.prange(int(N/n) + 1):
        T_i = c /np.log(2 + d * i)
        T[i *n:i * n+n] = T_i

    for iteration in tqdm(range(N)):
        
        move(config, iteration, energies)
        E[iteration] = config[2 * n][0]
    
    return config[0:n]

# Do 25 runs
for i in range(runs):
    sim(energies[i])
    df=pd.DataFrame({'energies':energies[i]})
    df.to_csv(r'data/logsim' + str(i) +'.csv', index = False)

x  = energies.mean(axis=0)
y = energies.std(axis=0)
df=pd.DataFrame({'mean':x,'std':y})
df.to_csv(r'data/meanstdlog.csv', index = False)


final_pos = sim()
x = 1


plt.plot(E)
plt.show()

theta = np.linspace(0, 2 * np.pi, 100)
x1 = np.cos(theta)
x2 = np.sin(theta)

# Temp
x = []
y = []
for pos in final_pos:
    x.append(pos[0])
    y.append(pos[1])

fig, axs = plt.subplots(1, 3)
axs[0].scatter(x, y)
axs[0].plot(x1, x2)
axs[0].set_title('Axis [0,0]')
axs[1].set_title('Axis [0,1]')
axs[1].plot(T)
axs[1].set_title('Axis [1,0]')
axs[2].plot(E)
plt.show()

accept_2 = [accept_i for accept_i in accept if accept_i != 1]
plt.scatter(range(len(accept_2)), accept_2)
plt.show()