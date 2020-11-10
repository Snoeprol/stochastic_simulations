import numpy as np
import matplotlib.pyplot as plt
n = 1000000

regular = []
var_reduc = []
g_s = []
hits = 0
while hits < 10000:
    
    # Accept reject
    u_1 = np.random.rand()
    u_2 = np.random.rand()
    if np.e**(-u_1) > u_2:
        hits += 1
        g_s.append(u_1)

for rn in g_s:

    g = (np.e / (np.e - 1)) * np.e**(-rn)
    f = 1
    h = np.exp(-(rn**2)) 
    
    var_reduc.append((f * h)/ g)

    u_1 = np.random.rand()
    g_2 = 1
    f_2 = 1
    h_2 = np.e**(-u_1**2)

    regular.append(f_2 * h_2)
print(np.mean(var_reduc))
print(np.var(var_reduc))
print(np.mean(regular))
print(np.var(regular))
print(1/np.e)
plt.hist(g_s, bins =50)
plt.show()
