import numpy as np

integral = 0
n = 100000
for x in range(n):
    u = np.random.uniform(0, 1)
    val = np.sin(u)

    integral += val

integral /= n

print(integral)
