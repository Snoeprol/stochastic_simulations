# Creates the plot for LB|LO

import numpy as np
import copy
import matplotlib.pyplot as plt
import datetime
from temperature import TemperatureList
from stepsize import StepsizeList
from numba import njit
from tqdm import tqdm


RADIUS = 1
PI = np.pi


class ParticleSystem:
    """
    Setup a system of point charges
    :param n: number of particles
    :param r: circle radius
    :param steps: number of iterations
    :param s0_list: Initial hillclimber list
    :return: 
    """

    def __init__(self, n, r, steps, s0_list, d=2):
        self.energies = []
        self.s0_list = s0_list
        self.r = r
        self.n = n
        self.d = d
        self.counter = 0
        self.create_configuration()
        self.steps = steps
        self.t_change = []
        self.s_change = []
        self.E1_total = 0

    def create_configuration(self):
        """
        Create initial configuration with random positions
        """
        self.current_config = np.zeros((self.n, self.d))
        for point_charge in range(self.n):
            angle = 2 * PI * np.random.rand()
            radius = self.r * np.random.rand()
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            self.current_config[point_charge][0] = x
            self.current_config[point_charge][1] = y

        self.E1 = calculate_total_energy(self.current_config)

    def move(self, T, S):
        """
        Moves all charges with random steps
        :param T: Temperature
        :param S: step size
        :return: Move particles
        """

        for i, charge in enumerate(self.current_config):
            x = charge[0]
            y = charge[1]
            rad = np.sqrt(x ** 2 + y ** 2)

            change = np.random.multivariate_normal([0, 0], np.array([[S, 0], [0, S]]))
            temp_x, temp_y = (
                self.current_config[i][0] + change[0],
                self.current_config[i][1] + change[1],
            )

            if temp_y ** 2 + temp_x ** 2 <= self.r ** 2:
                self.update_configs(T, S, temp_x, temp_y, i)

    def update_configs(self, T, S, temp_x, temp_y, i):
        """
        Move particles if new config better or movement accepted
        """
        E_1 = calculate_energy(
            [self.current_config[i][0], self.current_config[i][1]],
            i,
            self.current_config,
        )
        E_2 = calculate_energy([temp_x, temp_y], i, self.current_config)
        dE = E_2 - E_1

        if dE < 0:
            self.current_config[i][0] = temp_x
            self.current_config[i][1] = temp_y

        else:
            p = np.exp(-(E_2 - E_1) / S)

            U = np.random.rand()

            if p > U:
                self.E1_total = calculate_total_energy(self.current_config)

                self.current_config[i][0] = temp_x
                self.current_config[i][1] = temp_y

                E2_total = calculate_total_energy(self.current_config)
                s_i = -(E2_total - self.E1_total) / (np.log(U) * 10000)

                self.s0_list.pop(self.s0_list.index(max(self.s0_list)))
                self.s0_list.append(s_i)

    def simulate(self):
        """
        Do N simulations and write to csv file
        """
        for index in tqdm(range(self.steps)):

            S = max(self.s0_list)

            T = 0.5 / (np.log(2 + 0.2 * index))

            self.move(T, S)
            self.t_change.append(T)
            self.s_change.append(S)
            tot = calculate_total_energy(self.current_config)
            self.energies.append(tot)


@njit
def calculate_total_energy(list_particles):

    E_t = 0

    for i in range(0, len(list_particles)):

        for k in range(i + 1, len(list_particles)):
            distance = np.sqrt(
                (list_particles[i][0] - list_particles[k][0]) ** 2
                + (list_particles[i][1] - list_particles[k][1]) ** 2
            )

            E_t += 1 / distance

    return E_t


def calculate_energy(coordinates, particle_number, list_particles):

    E = 0

    for i in range(len(list_particles)):

        if i != particle_number:
            distance = np.sqrt(
                (coordinates[0] - list_particles[i][0]) ** 2
                + (coordinates[1] - list_particles[i][1]) ** 2
            )

            E += 1 / distance

    return E


M = 30000
temperatures = 1500
particles = 100
radius = 1

s = StepsizeList(particles, radius, temperatures, 0.99)
s0_list = s.generate_steps()

ps = ParticleSystem(particles, radius, M, s0_list)
energy = ps.simulate()

temperature_change = ps.t_change
step_change = ps.s_change

x = [item[0] for item in ps.current_config]
y = [item[1] for item in ps.current_config]

theta = np.linspace(0, 2 * np.pi, 200)
r = radius
x1 = r * np.cos(theta)
x2 = r * np.sin(theta)

fig, ax = plt.subplots(1, 3)
ax[0].set_title("Final configuration", fontsize=14.5)
ax[0].scatter(x, y)
ax[0].set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
ax[0].grid(which="major")
ax[0].set_xlim(-1.25, 1.25)
ax[0].set_ylim(-1.25, 1.25)
ax[0].plot(x1, x2)

ax[2].plot(ps.energies)
ax[2].set_xlabel("Steps", fontsize=14.5)
ax[2].set_title("Energy", fontsize=14.5)
ax[2].set_yticks([140, 120, 100, 80, 60])
ax[2].grid(which="major")

ax[1].plot(temperature_change)
ax[1].set_xlabel("Steps", fontsize=14.5)
ax[1].set_title("Temperature", fontsize=14.5)
ax[1].set_yticks([0, 0.25, 0.5, 0.75, 1])
ax[1].grid(which="major")
plt.show()
