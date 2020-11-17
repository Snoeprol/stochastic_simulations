import matplotlib.pyplot as plt
import random
import numpy as np
from tqdm import tqdm
from functions import Zn_1, sim


def LHS(n, coord_min, coord_max):
    dx = abs(coord_min - coord_max) / n
    lower = np.arange(coord_min, coord_max, dx)
    upper = np.arange(coord_min + dx, coord_max + dx, dx)

    if len(upper) != len(lower):
        upper = upper[:-1]

    points = np.random.uniform(low=lower, high=upper, size=[2, n]).T
    np.random.shuffle(points[:, 1])

    return points


def run_lhs(n, lim, coord_min, coord_max):
    gen_area = abs(coord_min - coord_max) ** 2

    points = LHS(n, coord_min, coord_max)
    xl = points[:, 0]
    yl = points[:, 1]
    c_list = []
    hit = 0

    for x, y in zip(xl, yl):

        in_mandel, c = sim(x, y, lim)

        if in_mandel:
            hit += 1

    return hit / n * gen_area

