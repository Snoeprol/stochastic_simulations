import numpy as np
n = 100
count = 0
wins = 0


def generate_point():
    x = np.random.rand()
    y = np.random.rand()
    if x**2 + y**2 < 1: return True 
    
    else: return False
'''
for i in range(n):
    x = np.random.rand()
    y = np.random.rand()
    if x**2 + y**2 < 1:
        count += 1
    print(count / (i + 1)- np.pi/4)
'''
# Pi 95% confidence +- 0.01
for i in range(n):
    lam = 1
    pi = 0
    x = []
    hits = 0
    count = 0
    stdev= 0
    while lam > 0.0025 or count < 100:
        if generate_point():
            hits += 1
            x.append(1)
        else:
            x.append(0)
        count += 1
        if len(x) % 99 == 0 : stdev = np.std(x)
        lam = stdev * 1.96 / np.sqrt(count)
    
    print(hits/count * 4 - np.pi)
    if abs(hits/count * 4 - np.pi) < 0.01:
       wins += 1 
    print(count)
print(wins/n)
