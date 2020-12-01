import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 18})
plt.rcParams["figure.figsize"] = [8.0, 6.0]
plt.rcParams["figure.dpi"] = 140

df = pd.read_csv (r'workloadvariance1.43.csv')
counts = df.values.T[0]

print('Mean:' + str(np.mean(counts)))
print('Standard deviation: ' + str(np.std(counts)))

print('confidence interval:' + str(np.std(counts) * 1.95 / np.sqrt(100)))
print('Relative confidence interval:' + str(np.std(counts) * 1.95 / np.sqrt(100)/np.mean(counts)))

# Plot workload vs rel ci
x= [0.33,0.42,0.57,0.70,0.89,0.95]
y = [0.0044,0.0042,0.0056,0.0062,0.016,0.036]

plt.scatter(x, y)
plt.xlabel(r'working load ($\rho$)')
plt.ylabel(r'Relative confidence interval')
plt.tight_layout()
plt.grid()
plt.show()