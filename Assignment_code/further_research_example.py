import matplotlib.pyplot as plt
import numpy as np
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

plt.xlabel('iterations')
plt.ylabel('points')
x = range(10)
random_x = []
random_y = []

for val in x:
    random_x.append(np.random.rand() + val)
    random_y.append(np.random.rand() + val)

random_y = np.array(random_y)
random_x = np.array(random_x)
s = 80
plt.scatter(random_x, random_y, s = s, label = 'Calculated optimal values')
plt.scatter(10 +  random_x, 10 +  random_y, s = s, label = 'Verification optimal values')
plt.plot(range(20), range(20), label = 'Predicted optimal values')
plt.legend()
plt.grid()
plt.show()