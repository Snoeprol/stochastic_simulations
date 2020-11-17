import matplotlib.pyplot as plt
import numpy as np 
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

samples =  100000

with open("probs_different_its.txt") as f:
    lines = f.readlines()
    
    values = np.zeros((2, len(lines)))
    for i, line in enumerate(lines):
        line = line.replace('\n', '')
        x = line.split(",")
        values[0][i] = float(x[0])
        values[1][i] = float(x[1])/samples * 6
        
deriv = np.diff(values[1])


# Create left and right axes objects
fig, axl = plt.subplots(figsize=(16,12))
axr = axl.twinx()
axl.set_xlabel('Iterations')

# Create left side line plot, color accordingly
color = "blue"
axl.plot(values[0], values[1], color=color)
axl.tick_params(axis="y", color=color, labelcolor=color)
axl.set_ylabel('Mandelbrot area')

# Create right side line plot, color accordingly
color = "red"
axr.semilogy(values[0][7:], deriv[6:],'-.', color=color)
axr.tick_params(axis="y", color=color, labelcolor=color)
axr.set_ylabel(r'$\frac{dA_{i,n}}{di}$')
plt.grid()
plt.show()


