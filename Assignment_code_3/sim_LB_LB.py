# Performs 25 simulations for LB|LB

from temperature import TemperatureList
from stepsize import StepsizeList
from tqdm import tqdm
from LB_LB import ParticleSystem

M = 30000
temperatures = 2800
steps = 2800
particles = 12
radius = 1


for _ in tqdm(range(25)):
    t = TemperatureList(particles, radius, temperatures, 0.99)
    t0_list = t.generate_temperature()
    s = StepsizeList(particles, radius, steps, 0.99)
    s0_list = s.generate_steps()

    ps = ParticleSystem(particles, radius, M, t0_list, s0_list)
    energy = ps.simulate()
