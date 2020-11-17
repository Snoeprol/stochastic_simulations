import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
from functions import Zn_1, sim


def ortho(n):
    m = 0
    xl = []
    yl = []
    xlist = np.zeros((n, n))
    ylist = np.zeros((n, n))
    scale = 4 / n ** 2

    for i in range(n):
        for j in range(n):
            m += 1
            xlist[i][j] = m
            ylist[i][j] = m

    for y in range(n):
        np.random.shuffle(xlist[y])
        np.random.shuffle(ylist[y])

    for i in range(n):

        for j in range(n):

            x = -2.0 + scale * (xlist[i][j] + np.random.uniform(0, 1))
            y = -2.0 + scale * (ylist[j][i] + np.random.uniform(0, 1))

            xl.append(x)
            yl.append(y)

    return xl, yl


def run_ortho(n, lim, coord_min, coord_max):
    gen_area = abs(coord_min - coord_max) ** 2
    xl, yl = ortho(n)

    c_list = []
    hit = 0

    for x, y in zip(xl, yl):

        in_mandel, c = sim(x, y, lim)

        if in_mandel:
            hit += 1
            c_list.append(c)

    return hit / n ** 2 * gen_area

