# Performs 25 simulations for LB|LO

from stepsize import StepsizeList
from tqdm import tqdm
from LB_LO import ParticleSystem

M = 30000
temperatures = 2800
particles = 12
radius = 1

for _ in tqdm(range(25)):
    s = StepsizeList(particles, radius, temperatures, 0.99)
    s0_list = s.generate_steps()

    ps = ParticleSystem(particles, radius, M, s0_list)
    energy = ps.simulate()

