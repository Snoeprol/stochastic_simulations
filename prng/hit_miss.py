import numpy as np
n = 100
count = 0
wins = 0
runs = 100

def generate_point():
    x = np.random.rand()
    y = np.random.rand()
    if x**2 + y**2 < 1: return True 
    
    else: return False

def generate_pi(n):
    hits = 0
    for i in range(n):
        if generate_point():
            hits += 1
    return hits/n * 4

# Pi 95% confidence +- 0.01
for _ in range(runs):
    lam = 1
    pis = []
    stdev= 0
    count = 0
    while lam > 0.01:
        count += 1
        pis.append(generate_pi(100))
        stdev = np.std(pis)
        if count > 2: lam = stdev * 1.96 / np.sqrt(count)
    theta = np.mean(pis)
    print(theta)
    print(np.pi - theta)
    print(count)
    if np.pi - theta < 0.01:
        wins += 1
print(wins/runs)
