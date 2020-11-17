# This code measures the time of sim() which is a random sampling method for a meshgrid of data to produce
# a matrix of computational time values.

from lhs import sim, Zn_1
import matplotlib.pyplot as plt
import numpy as np
import time
from tqdm import tqdm


def timing(function):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = function(*args, **kwargs)
        time2 = time.time()
        return time2 - time1

    return wrap


@timing
def function(i, N):

    hit = 0
    for _ in range(N):
        x = np.random.uniform(-2, 2)
        y = np.random.uniform(-2, 2)

        in_mandel, c = sim(x, y, i)

        if in_mandel:
            hit += 1
    return 0


# 100 x 100 matrix. Higher values yield a finer grid
m = 100
rows, cols = (m, m)

i = np.array([2 * x for x in range(1, m + 1)])
n = np.array([1000 * x for x in range(1, m + 1)])
C = [[0 for i in range(cols)] for j in range(rows)]

for x, i_ in enumerate(tqdm(i)):
    for y, n_ in enumerate(n):
        C[x][y] = function(i_, n_)

file = open("data/matrix.txt", "a")
file.write(str(C))
file.close()
