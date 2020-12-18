import numpy as np
import numba
from numba import njit
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd

TAU = np.sqrt(0.0001)

N = 1000000
T = np.zeros((N, 1))
n = 12
E = np.zeros((N, 1))
c = 2
c_0 = 0
runs = 25
config = np.zeros((2*n + 1,2))
accept = np.zeros(N)
energies = np.zeros((runs, N))

@njit
def accept_reject(config, i, energies):
    
    dE = config[2*n][1] - config[2*n][0]

    if dE < 0:
        config[:n] = config[n:2*n] + 0
        config[2 * n][0] = config[2 * n][1] + 0
    else:
        U = np.random.rand()
        if U < np.exp(-dE/T[i]):
            config[:n] = config[n:2*n] + 0
            config[2 * n][0] = config[2 * n][1] + 0
        else:
            config[n:2*n] = config[:n] + 0
    energies[i] = config[2*n][0] + 0

@njit 
def move(config, iteration, energies):
    """Find the maximum value in values and store in result[0]"""
    
    # Compute pi by drawing random (x, y) points and finding what
    # fraction lie inside a unit circle
    inside = 0
    config[n:2*n] = config[:n] + 0
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


def sim(energies, its):

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
    
    for i in range(int(its/n) + 1):
        T_i = c * ((1 - i/(int(its/n) + 1))) + c_0
        T[i *n:i * n+n] = T_i


    for iteration in tqdm(range(its)):
        
        move(config, iteration, energies)
        E[iteration] = config[2 * n][0]

    
    return config


# Make 25 simulations for linear temperature
for i in range(runs):
    sim(energies[i], N)
    df=pd.DataFrame({'energies':energies[i]})
    df.to_csv(r'data/linsim' + str(i) +'newenergy.csv', index = False)

x  = energies.mean(axis=0)
y = energies.std(axis=0)
df=pd.DataFrame({'mean':x,'std':y})
df.to_csv(r'data/meanstdlinnewtemp.csv', index = False)


plt.rcParams.update({'font.size': 22})
Numbers = [2 **k for k in range(18)]
energies_2 = np.zeros((18,1))
for i, run in enumerate(Numbers):
    energies_2[i] = sim(energies[i], run)[2*n,0]

print(energies_2)
plt.scatter(Numbers, energies_2, label = 'Iterated point')
plt.plot(Numbers, energies_2)
plt.xlabel('total iterations')
plt.ylabel('Final energy [a.u.]')
plt.grid()
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()

# Single simulation
result = sim(energies[0], N)
final_pos = result[0:n]

theta = np.linspace(0, 2 * np.pi, 100)
x1 = np.cos(theta)
x2 = np.sin(theta)

# Temp
x = []
y = []
for pos in final_pos:
    x.append(pos[0])
    y.append(pos[1])

plt.scatter(x,y, label = 'Particles')
plt.plot(x1, x2,  color = 'red',label ='Confinement circle')
plt.title('Final configuration')
plt.grid()
plt.legend(loc = 'upper right')
plt.show()

fig, axs = plt.subplots(1, 3)
axs[0].scatter(x, y)
axs[0].plot(x1, x2)
axs[0].grid()
axs[0].set_title('Final configuration')
axs[1].set_title('Temperature')
axs[1].grid()
axs[1].set_xlabel('Steps')
axs[1].plot(T)
axs[2].set_title('Energy')
axs[2].set_xlabel('Steps')
axs[2].set_ylabel('Energy [a.u.]')
axs[2].plot(E)
axs[2].grid()
plt.show()
