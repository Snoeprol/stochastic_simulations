import numpy as np
import copy
import matplotlib.pyplot as plt
import datetime
from temperature import TemperatureList
from stepsize import StepsizeList
from tqdm import tqdm
from numba import njit


RADIUS = 1
PI = np.pi


class ParticleSystem:
    """
    Setup a system of point charges
    :param n: number of particles
    :param r: circle radius
    :param steps: number of iterations
    :param t0_list: Initial temperature list
    :return: 
    """

    def __init__(self, n, r, steps, t0_list, d=2):
        self.r = r
        self.n = n
        self.d = d
        self.counter = 0
        self.t0_list = t0_list
        self.create_configuration()
        self.steps = steps
        self.t_change = []
        self.s_change = []
        self.energies = []
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

        self.s_change.append(S)

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
                self.update_configs(T, temp_x, temp_y, i)

    def update_configs(self, T, temp_x, temp_y, i):
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
            p = np.exp(-(E_2 - E_1) / T)
            U = np.random.rand()

            if p > U:
                self.E1_total = calculate_total_energy(self.current_config)

                self.current_config[i][0] = temp_x
                self.current_config[i][1] = temp_y

                E2_total = calculate_total_energy(self.current_config)

                t_i = -(E2_total - self.E1_total) / np.log(U)
                print(self.t, (E2_total - self.E1_total))

                if dE != 0:
                    self.t0_list.pop(self.t0_list.index(max(self.t0_list)))
                    self.t0_list.append(t_i)

    def simulate(self):
        """
        Do N simulations and write to csv file
        """
        f = open("energy_L_LB2.csv", "a")

        for index in range(self.steps):

            T = max(self.t0_list)
            S = 0.1 - 0.1 / self.steps * index

            self.move(T, S)
            self.t_change.append(T)
            self.s_change.append(S)
            tot = calculate_total_energy(self.current_config)
            self.energies.append(tot)
            f.write(str(tot) + "\n")

        f.close()


@njit
def calculate_total_energy(list_particles):
    """
    Calculate the total energy 
    :param list_particles: list of all particles with positions [[x,y]]
    :return: Energy total
    """

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
    """
    Calculate the total energy 
    :param coordinates: coordinates of moved particles
    :param particle_number: Particle index
    :param list_particles: list of all particles with positions [[x,y]]
    """
    E = 0

    for i in range(len(list_particles)):

        if i != particle_number:
            distance = np.sqrt(
                (coordinates[0] - list_particles[i][0]) ** 2
                + (coordinates[1] - list_particles[i][1]) ** 2
            )

            E += 1 / distance

    return E
