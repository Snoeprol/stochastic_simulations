import numpy as np
import matplotlib.pyplot as plt

theta = np.pi


def sim():
    hit = 0
    for _ in range(100):
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)

        r = x ** 2 + y ** 2

        if r <= 1:
            hit += 1

    return 4 * hit / 100


def dif(x):
    return (x - avarage) ** 2


n = 10
d = 1

avarage_sum = 0
avarage = 0
rv_list = []

for _ in range(10):
    x_i = sim()
    rv_list.append(x_i)
    avarage_sum += x_i

avarage = avarage_sum / n
s = np.sqrt(sum(list(map(dif, rv_list))) / (n - 1))
d = 1.96 * s / np.sqrt(n)

while not (d < 0.01):

    x_i = sim()
    rv_list.append(x_i)
    avarage_sum += x_i
    n += 1

    avarage = avarage_sum / n
    s = np.sqrt(sum(list(map(dif, rv_list))) / (n - 1))

    d = 1.96 * s / np.sqrt(n)

    upper = avarage + d
    lower = avarage - d

print("Simulation count: ", n)
print("Pi on interval [" + str(lower) + ", " + str(upper) + "], with confidence 95%")

# Calculate MSE between total sample set estimator and bootstrap estimator, bootstrap size of total sample set
bootstrap_size = len(rv_list)
boostraps = 50
bootstrap_sets = []
bootstrap_medians = []
total_sample_mean = np.mean(rv_list)

for _ in range(boostraps):
    # Random choice WITH replacement
    bootstrap_sample = [np.random.choice(rv_list) for _ in range(bootstrap_size)]
    bootstrap_medians.append(np.mean(bootstrap_sample))
    bootstrap_sets.append(bootstrap_sample)

# Bootstrap estimate of variance
unbiased_bootstrap_variance = np.var(bootstrap_medians, ddof=1)
unbiased_total_sample_mean = np.var(rv_list, ddof=1)
bootstrap_mean = np.mean(bootstrap_medians)

print("Bootstrap estimate of variance: " + str(unbiased_bootstrap_variance))
print("Variance of total sample set: " + str(unbiased_total_sample_mean))
print("Bootstrap mean: " + str(bootstrap_mean))

# MSE
MSE_list = [(m - total_sample_mean) ** 2 for m in bootstrap_medians]
MSE = np.mean(MSE_list)

b_lower = total_sample_mean - 1.96 * np.sqrt(unbiased_bootstrap_variance)
b_upper = total_sample_mean + 1.96 * np.sqrt(unbiased_bootstrap_variance)

print("Bootstrap MSE between total sample set and bootstrap medians: " + str(MSE))
print(
    "Bootstrap interval ["
    + str(b_lower)
    + ", "
    + str(b_upper)
    + "], with confidence 95%"
)

