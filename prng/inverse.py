import numpy as np
import matplotlib.pyplot as plt


def X(u):
    if u < 0.17:
        return 0
    elif 0.17 <= u < 0.36 + 0.17:
        return 1
    elif 0.36 + 0.17 <= u < 0.36 + 0.17 + 0.31:
        return 2
    elif 0.36 + 0.17 + 0.31 <= u < 0.36 + 0.17 + 0.31 + 0.13:
        return 3
    elif 0.36 + 0.17 + 0.31 + 0.13 <= u < 0.36 + 0.17 + 0.31 + 0.13 + 0.03:
        return 4


ul = []
for _ in range(1000):
    unew = X(np.random.uniform(0, 1))
    ul.append(unew)

plt.hist(ul, bins=5)
plt.show()
