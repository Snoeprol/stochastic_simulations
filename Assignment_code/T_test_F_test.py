import numpy as np
from scipy.stats import ttest_ind
from scipy.stats import fisher_exact
from scipy.stats import f as fisher_f
import matplotlib.pyplot as plt
import scipy.integrate as integrate

random_areas = []
lhs_areas = []

# Get values from files
with open("random_areas.txt") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip("\n")
        area = float(line)
        random_areas.append(area)

with open("areas_lhs.txt") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip("\n")
        area = float(line)
        lhs_areas.append(area)

# Perform T-test
test = ttest_ind(random_areas, lhs_areas, equal_var=False, axis=0)

print("value of T-test: " + str(test))

# Interval on which to generate pdf.
x = np.linspace(0, 15, 1001)[1:]

# Generate distribution and actual value and plot
mu = 0
ls = '-'

dist = fisher_f(len(lhs_areas), len(random_areas), mu)
plt.plot(x, dist.pdf(x), ls=ls, c='black', label = 'Fischer distribution')
print(sum(dist.pdf(x[0:750]) * 15/1001))
actual = max([np.var(random_areas)/np.var(lhs_areas), np.var(lhs_areas)/np.var(random_areas)])
plt.vlines(actual, ymin = -10, ymax = 10,ls = '-.', label = 'Actual value')

plt.xlim(0, 12)
plt.ylim(0.0, 10)

plt.xlabel('$x$')
plt.ylabel(r'$p(x|d_1, d_2)$')
plt.title("Fisher's Distribution")

plt.legend()
plt.show()