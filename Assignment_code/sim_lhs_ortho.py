# Simulates the orthogonal and LHS method to calculate the area of the mandelbrot, and saves the values to a textfile

import numpy as np
import matplotlib.pyplot as plt
from lhs import LHS, run_lhs
from functions import sim, Zn_1
from ortho import ortho, run_ortho
from tqdm import tqdm

N = [4, 8, 11, 23, 32, 71, 101, 225, 317]
lim = 100

file1 = open("data/variance_ortho.txt", "a")
file2 = open("data/variance_lhs.txt", "a")
file1m = open("data/mean_ortho.txt", "a")
file2m = open("data/mean_lhs.txt", "a")

for _ in range(10):
    for points in tqdm(N):
        coord_min = -2 + 4 / points ** 2
        coord_max = -2 + 4 / points ** 2 * (points ** 2 + 1)

        areas_ortho = []
        areas_lhs = []

        for _ in range(100):
            ortho_area = run_ortho(points, lim, coord_min, coord_max)
            lhs_area = run_lhs(points ** 2, lim, coord_min, coord_max)

            areas_ortho.append(ortho_area)
            areas_lhs.append(lhs_area)

        file1.write(str(points) + "," + str(np.var(areas_ortho)) + "\n")
        file1m.write(str(points) + "," + str(np.mean(areas_ortho)) + "\n")

        file2.write(str(points) + "," + str(np.var(areas_lhs)) + "\n")
        file2m.write(str(points) + "," + str(np.mean(areas_lhs)) + "\n")

file1.close()
file1m.close()
file2.close()
file2m.close()
