import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import matplotlib
from scipy.stats import chisquare
from scipy.stats import chi2

# Set matplotlib settings
matplotlib.rcParams.update({'font.size': 18})
plt.rcParams["figure.figsize"] = [8.0, 6.0]
plt.rcParams["figure.dpi"] = 140

# Get data
df = pd.read_csv (r'data/shortfirst.csv')
counts = df.values.T[0]
bins_values = plt.hist(counts, bins=20)
plt.grid()

# Get fitted mu and std.
mu, std = norm.fit(counts)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 10)

# Get pdf
p = norm.pdf(x, mu, std)
plt.plot(x, p, "k", linewidth=2)

plt.show()

# Sample std.
std = np.std(counts)

# Lambda for 95% confidence
lambda_confidence = 1.96

mean = np.mean(counts)
interval = lambda_confidence * std / np.sqrt(len(counts))

# 95% conf interval
print("Mean:", mean)
print("Std", str(interval))


def normal(x, mean, sd):
    prob_density = (1 / (2 * np.pi * sd ** 2)) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


# Chi-squared test
actual_vals = bins_values[0]
bins = bins_values[1]


x = [(bin + bins[i + 1]) / 2 for i, bin in enumerate(bins[0 : len(bins) - 1])]
y = actual_vals


# FILL IN OWN ESTIMATIONS FOR VALS
n = len(x)  # the number of data
mean = mu  # note this correction
sigma = std  # note this correction
peak_height = 140


def gaus(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))


popt, pcov = curve_fit(gaus, x, y, p0=[peak_height, mean, sigma])

y_fit = gaus(x, *popt)
plt.plot(x, y, "b+:", label="data")
plt.plot(x, y_fit, "ro:", label="fit")
plt.legend()
plt.title("Random sampling queue-time distribution and fit")
plt.xlabel("Average queue-time [1]")
plt.ylabel("Frequency [1]")
plt.grid()
plt.show()

# Chi-squared by hand
chi_squared = 0
actual_vals = np.array(actual_vals)
expected = y_fit
for i, expected_value in enumerate(expected):
    chi_squared += (expected_value - actual_vals[i]) ** 2 / expected_value

# for item in zip(actual_vals, expected):
#     print(item)
crit = chi2.ppf(0.95, df=1000 - 1)
print("Chi squared: ", chi_squared)
print("Critical value: ", crit)

# Premade chi-squared test
print(y_fit)
print("Premade Chi square :", chisquare(actual_vals, expected))
