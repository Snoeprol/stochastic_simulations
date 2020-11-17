
import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit

def pol(X, a, b, c, d, e, f, g, h, i):
    x_i , x_n = X
    return a + b * x_i + c * x_n + d * x_i**2 + e * x_i**2 * x_n + f * x_n **2 * x_i **2 + g * x_n**2 + h * x_i * x_n**2 + i * x_i * x_n

import numpy as np
from mpl_toolkits import mplot3d 
import numpy as np 
import matplotlib.pyplot as plt 

fig = plt.figure(figsize =(14, 9)) 
ax = plt.axes(projection ='3d') 

x = np.linspace(0, 1, 20)
y = np.linspace(0, 1, 20)
X, Y = np.meshgrid(x, y, copy=False)
Z = X**2 + Y**2 + np.random.rand(*X.shape)*0.01
Z = X**2 + Y**2 
print(Z.shape)
ax.plot_surface(X, Y, Z) 
X = X.flatten()
Y = Y.flatten()

A = np.array([X*0+1, X, Y, X**2, X**2*Y, X**2*Y**2, Y**2, X*Y**2, X*Y]).T
print(A.shape)
B = Z.flatten()

coeff, r, rank, s = np.linalg.lstsq(A, B)

print(coeff)
  

# Creating dataset 
x = x.T
y = y# transpose 
X, Y = np.meshgrid(x,y)
zs = np.array(pol((X, Y), 4.64166278e-03, -1.27074797e-03,  3.74382400e-03,  1.00275941e+00,5.27967359e-05, -5.62338644e-03,  9.95474495e-01,  1.25280088e-02, -7.34284869e-03))
Z = zs.reshape(X.shape)

print(Z.shape, X.shape, Y.shape)
ax.plot_surface(x, y.T, Z)

sdasd = pol((1,0),4.64166278e-03, -1.27074797e-03,  3.74382400e-03,  1.00275941e+00,5.27967359e-05, -5.62338644e-03,  9.95474495e-01,  1.25280088e-02, -7.34284869e-03)

z = (np.array(pol((X,Y), 4.64166278e-03, -1.27074797e-03,  3.74382400e-03,  1.00275941e+00,5.27967359e-05, -5.62338644e-03,  9.95474495e-01,  1.25280088e-02, -7.34284869e-03)))
print(z)  
# Creating figyre 

  
# Creating plot 
#ax.plot_surface(x, y, z) 
  
# show plot 
plt.show() 



i_s = np.linspace(0,1,25)
n_s = np.linspace(0,1,25)
combo = np.append(i_s, n_s)
c_s = np.random.uniform(-5,5, size = (25,1))
# load a, b, c
# guess initial values for p0, e0, p1, e1, p2, e2
def combo_pol(combo_data, a, b, c, d, e, f, g):

    x_i = combo_data[: len(i_s)]  # first data
    x_n = combo_data[len(n_s) :]  # second data
    return a + b * x_i + c * x_n + d * x_i * x_n + e * x_i**2 + f * x_n **2 + g * x_n**2 * x_i**2



popt, pcov = curve_fit(combo_pol, combo, c_s)
print(popt)