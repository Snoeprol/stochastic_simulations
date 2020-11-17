import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 15})
all_values = []

with open("matrix.txt", "r") as f:

    for line in f:
        data = line.split(",")
        values = [float(num) for num in data]
        all_values.append(values)

flat_values = all_values[0]

new_matrix = []
temp = []

for i, entry in enumerate(flat_values):
    temp.append(entry)

    if (i + 1) % 100 == 0:
        new_matrix.append(temp)
        temp = []
array_matrix = np.array(new_matrix)

fig = plt.figure(figsize=(12, 7))
ax = plt.axes(projection="3d")
m = 100
i = np.array([2 * x for x in range(1, m + 1)])
n = np.array([1000 * x for x in range(1, m + 1)])
I, N = np.meshgrid(i, n)


Z = array_matrix.reshape(I.shape)

ax.plot_surface(I, N, Z)
ax.set_xlabel("i", labelpad=10)
ax.set_ylabel("S", labelpad=10)
ax.set_zlabel("C", labelpad=10)

ax.set_title("Computational time in seconds:")
plt.show()
