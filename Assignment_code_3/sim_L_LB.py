# Performs 25 simulations for L|LB

from temperature import TemperatureList
from tqdm import tqdm
from L_LB import ParticleSystem

M = 30000
temperatures = 2800
particles = 12
radius = 1

for _ in tqdm(range(25)):

    t = TemperatureList(particles, radius, temperatures, 0.99)
    t0_list = t.generate_temperature()

    ps = ParticleSystem(particles, radius, M, t0_list)
    energy = ps.simulate()

