import numpy as np
import matplotlib.pyplot as plt


xn_prev = 2
n = 10000
a = 31792125
m = 268435399
c = 4
distance = 0

x = []
xd = []

for _ in range(n):
    xn = (a * xn_prev + c) % m
    distance = abs(xn - xn_prev)
    x.append(xn / m)
    xd.append(distance / m)
    xn_prev = xn

fig, axs = plt.subplots(1, 2)
axs[0].hist(x, bins=100)
axs[1].hist(xd, bins=100)
plt.show()
