import matplotlib.pyplot as plt
import random
import numpy as np
from tqdm import tqdm

def Zn_1(z_n, c):
    '''Calculates next step for 
    a candidate in Mandelbrot set'''
    return z_n ** 2 + c

def iterate_over_random_candidate(i):
    '''Generates possible candidate and determines
    whether or not the candidate diverged after i iterations'''
    converger = 0
    z = 0

    # Create candidate
    c1 = random.uniform(-2, 1)
    c2 = random.uniform(-1, 1)
    c = complex(c1, c2)

    # Shifted norm
    norm = np.sqrt((c1 + 0.2887)**2 + c2**2)

    while converger < i:
        z_n1 = Zn_1(z, c)

        if abs(z_n1) < 2:
            z = z_n1
            converger += 1

        else:
            break
    
    return (converger, c, norm)

if __name__ == "__main__":
    n = 5000
    simulations = 1000
    iterations = 100

    # Lists with average areas and norms per run
    areas = []
    all_norms = []

    # Do simulations
    for i in tqdm(range(simulations)):
        count = 0
        z_list = []
        norms = []
        for x in range(n):

            converger, z, norm = iterate_over_random_candidate(iterations)
            norms.append(norm)
            if converger > iterations - 1:
                count += 1
        areas.append(count/n * 6)
        all_norms.append(np.mean(norms))

    # Averages
    average_area = np.mean(areas)
    average_norm = 0.9832

    # Variances
    variance_norms = 0.1485/n
    variance_areas = np.var(areas)

    # Calculate covariance
    mean_y = average_norm
    mean_x = sum(areas)/ len(areas)

    cov = sum((a - mean_x) * (b - mean_y) for (a,b) in zip(areas,all_norms)) / len(areas)

    # E[Z] = E[X] - Cov[X,Y] / Var[Y] (E[Y] - mu_Y)
    Z = average_area - cov / variance_norms * (np.sum(np.array(all_norms) - average_norm))
    var_Z = np.var(areas) - cov**2 / variance_norms

    print("Variance of Z: " + str(var_Z))
    print("Variance of X: " + str(variance_areas))
    print("Var X/ Var Z: " + str(np.var(areas)/ var_Z))
    print(areas)

    with open('random_areas.txt', 'w') as f:
        for item in areas:
            f.write("%s\n" % item)