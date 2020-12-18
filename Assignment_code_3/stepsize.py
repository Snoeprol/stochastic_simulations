import numpy as np
import random
from numba import njit

RADIUS = 1
CHARGES = 5
PI = np.pi
energies = []


class StepsizeList:
    """
    Creates the initial list for the hill-climber
    :param n: number of particles
    :param r: circle radius
    :param Lmax: List size
    :param p0: starting acceptance probability
    """

    def __init__(self, n, r, Lmax, p0, d=2):
        self.r = r
        self.n = n
        self.d = d
        self.p0 = p0
        self.E_start = 0
        self.create_configuration()
        self.stepsize_list = [0.1]
        self.E1_total = 0
        self.Lmax = Lmax

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
        self.E_start = calculate_total_energy(self.current_config)

    def move(self):
        """
        Moves all charges with random steps
        :return: Move particles
        """

        charge = random.sample(list(enumerate(self.current_config)), 1)[0]

        i = charge[0]
        x = charge[1][0]
        y = charge[1][1]

        rad = np.sqrt(x ** 2 + y ** 2)
        stepsize = np.array([[0.0001, 0], [0, 0.0001]])
        change = np.random.multivariate_normal([0, 0], stepsize)
        temp_x, temp_y = (
            self.current_config[i][0] + change[0],
            self.current_config[i][1] + change[1],
        )

        if temp_y ** 2 + temp_x ** 2 <= self.r ** 2:
            self.update_configs(temp_x, temp_y, i)

    def generate_steps(self):
        """
        Generates the list for the hillclimber
        """

        for _ in range(self.Lmax):

            self.move()

        return self.stepsize_list

    def update_configs(self, temp_x, temp_y, i):
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
        tot = calculate_total_energy(self.current_config)
        U = np.random.rand()

        if dE < 0:

            self.current_config[i][0] = temp_x
            self.current_config[i][1] = temp_y

            s = -abs(E_2 - E_1) / (np.log(self.p0) * 10000)
            self.stepsize_list.append(s)

        else:

            s = -abs(E_2 - E_1) / (np.log(self.p0) * 10000)
            self.stepsize_list.append(s)


def calculate_energy(coordinates, particle_number, list_particles):
    """
    Calculate the total energy 
    :param coordinates: coordinates of moved particles
    :param particle_number: Particle index
    :param list_particles: list of all particles with positions [[x,y]]
    :return: Energy of movement
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


@njit
def calculate_total_energy(list_particles):
    """
    Calculate the total energy 
    :param list_particles: list of all particles with positions [[x,y]]
    :return: Energy total
    """

    E = 0

    for i in range(0, len(list_particles)):

        for k in range(i + 1, len(list_particles)):

            distance = np.sqrt(
                (list_particles[i][0] - list_particles[k][0]) ** 2
                + (list_particles[i][1] - list_particles[k][1]) ** 2
            )
            E += 1 / distance

    return E

