import numpy as np

n = 500
samples = 1000
r = 100

def generate_point():
    x = np.random.rand()
    y = np.random.rand()
    if x**2 + y**2 < 1: return True 
    
    else: return False

def calc_pi(n):
    count = 0
    for _ in range(n):
        if generate_point():
            count += 1
    return count/n * 4

pis = []
for i in range(n):
    pis.append(calc_pi(n))
    
theta = sum(pis)/n

Y_s = []
for i in range(r):
    #Random choice from values of pi
    Y_i = [np.random.choice(pis) for _ in range(n)]
    # Sum and divide by n to get a value 
    Y_i = (sum(Y_i)/n - theta)**2
    Y_s.append(Y_i)

MSE = sum(Y_s)/r
print(np.sqrt(MSE))
print("Estimated interval = " + str(theta - np.sqrt(MSE)) + "," + str(theta + np.sqrt(MSE)) )
