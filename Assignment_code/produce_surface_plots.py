# Code for producing Figure 3, 4 and 5 in the report
# This consists of the surface plots, and a slice at a
# particular computational time and compare variances

import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import colorsys
from matplotlib.colors import ListedColormap
import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from readmatrix import read_matrix

# Part 1: Making surface plot of computational time and fit

# Values for which we performed iterations
m = 100
i = np.array([2 * x for x in range(1, m + 1)])
n = np.array([1000 * x for x in range(1, m + 1)])
i = np.array([x for x in i])
n = np.array([x for x in n])
X, Y = np.meshgrid(i, n, copy=False)


# READ DATA
array = read_matrix()
Z = array
data = Z.reshape(X.shape)

X = X.flatten()
Y = Y.flatten()
A = np.array([X*0+1, X, Y, X**2, Y**2]).T
B = Z.flatten()

coeff, r, rank, s = np.linalg.lstsq(A, B)

# The polynomial fitted to the data
def pol(X, a, b, c, d, e):
    '''returns value of 2d polynomial
    given by equation (3) in the report,
    with coefficients a, b, c, d, e'''
    x_i, x_n = X
    return (
        a
        + b * x_i
        + c * x_n
        + d * x_i ** 2
        + e * x_n**2
    )

# Prepare plot
fig = plt.figure(figsize=(14, 9))
ax = plt.axes(projection="3d")


x = i
y = n  
X, Y = np.meshgrid(x, y)

zs = np.array(
    pol(
        (X, Y),
    # FOUND FITTING COEFFICIENTS
    -5.86299690e-01,
    9.30264360e-03,
    1.14173892e-05,
    3.63603118e-07,
    5.08596777e-11
    )
)
Z = zs.reshape(X.shape)

ax.plot_surface(X, Y, Z, color = 'red', label = 'Fit', cmap=cm.Spectral)
ax.plot_surface(X, Y, data, color = 'blue', label = 'Data',  cmap=cm.cool_r)
plt.xlabel('Iterations', labelpad=30)
plt.ylabel('Points', labelpad=30)
plt.title('Computational time [s]')
plt.show()

# Part 2: Calculating optimal i and n for given computational time

# computational time
c = 1.5

X, Y = np.meshgrid(x,y)
z = zs


plot = plt.contour(X,Y,(c - z),[0])

points = []
variances = []
for point in plot.allsegs[0][0]:
    # Get the points at which the computational time is equal in the fit
    points.append(point)

# IF ALL VARIANCES AVAILABLE IMPORT UNDER THIS COMMENT as matrix all_variances[i][n] variance

# Get the closest actual value, to associate variance with point (if variances are available)
try:
    for point in points:
        i = min(x, key=lambda x:abs(x-point[0]))
        n = min(y, key=lambda x:abs(x-point[0]))
        index_i = np.where(x == i)[0][0]
        index_n = np.where(y == n)[0][0]
        variances.append(all_variances[index_i][index_n])
except:
    print('all_variances list is empty!')
    variances = np.array([0.0002811631971536462, 0.00012087111111111154, 0.00035753743906204584, 0.0003864954016620491, 8.751689999999915e-05, 0.0003344164997846756, 0.0002960073469387753, 0.00034103412511166987, 0.00018537322314049666, 0.00022685267638331737, 0.00012482880907372512, 0.00021122562500000032, 0.00011482037796721258, 0.00019214726400000132, 0.0002363894350521666, 0.000418814733727811, 0.00017769124544481609, 0.00020992592592592387, 0.00023157734693877568, 0.0001724871743350828, 0.00010897769322235434, 8.650752452978441e-05, 0.00023867560000000106, 0.00018628325758248898, 
    0.00018326509885535942, 0.00012905472656250065, 0.00012825674629987507, 0.00013413851239669447, 0.00021431533408005152, 0.0004952292041522487, 0.0004918767559051295, 0.0002316389877551027, 
    6.477638021485957e-05, 0.0004140358333333327, 0.00012916242512783034, 0.00019017666180777087, 3.4874127423822604e-05, 8.695745921819196e-05, 0.00021557041420118428, 0.00031465241446798967, 
    0.00011673562500000075, 8.406391820559994e-05, 5.5565496728138115e-05, 8.745795918367427e-05, 0.00018071643533908724, 0.00010384588426176283, 9.613347735031263e-05, 0.00017441330578512457, 
    0.00010233127437825626, 0.00019348639999999955, 0.00012482908848744325, 0.00018047977315689906, 0.0001958167084565194, 6.018868134047121e-05, 9.107912505836068e-05, 9.654027046780502e-05, 8.418646671316732e-05, 0.00011380059033627077, 0.00022079158858165663, 0.0001660127778090079, 0.0002058433005361467, 2.6809287649668476e-05, 0.00017631782299915374, 0.00017044932548664608, 0.00013352955034844633, 0.00015341703125000002, 4.654471350976041e-05, 5.890205747605276e-05, 0.0001979163544859205, 0.0001067364000000001, 0.00010571979107278319, 7.442560553633161e-05, 0.0001242910650887572, 0.00012550548299677716, 0.00014587638305446924, 0.00013521790661020846, 9.410925925925912e-05, 0.0001215420174913709, 0.000267747649586776, 6.995138811420817e-05, 6.179464285714345e-05, 9.601147052914393e-05, 0.00012568598337950044, 0.00012124101162062502, 7.719977407847828e-05, 0.00016791804573294903, 6.393748922723353e-05, 5.9300665772867336e-05, 0.00010186959999999852, 6.128517190273287e-05, 8.996962106960536e-05, 0.00013674546832101803, 4.406918834547399e-05, 4.788040435262105e-05, 0.00012333061224489657, 5.8786232997273706e-05, 8.486551757812364e-05, 5.4147493491124553e-05, 6.535810238243882e-05, 0.0001264211570247935, 0.00011607605889054277, 0.0001312110581421269, 9.206235596308517e-05, 0.00018759620242214493, 5.8666999283540474e-05, 9.392370510396854e-05, 7.177763840355768e-05, 1.33335918367345e-05, 6.232019179057443e-05, 7.563535012894346e-05, 0.00011163445517191784, 0.00013332333333333318, 9.384407722152471e-05, 8.706041658847843e-05, 6.795721817105113e-05, 8.287290723155636e-05, 5.824594583774073e-05, 5.487974400000047e-05, 4.867638460516279e-05, 6.936238919667569e-05, 9.140168002773997e-05, 4.8197132737392366e-05, 0.00010754348313929165, 9.850538461538413e-05, 3.1364933293449075e-05, 9.451508412113409e-05, 0.000190094639192909, 2.5916850000000107e-05, 3.9740445316494396e-05, 6.868182925289228e-05, 6.83105208005173e-05, 4.14638814890335e-05, 8.695944307895374e-05, 4.099206277686194e-05, 5.489777399899458e-05, 0.00012623330980049538, 7.00630609545226e-05, 9.229594320117895e-05, 7.945618655692847e-05, 6.2761158931668e-05, 7.069813206424804e-05, 0.00011945537747721772, 6.233743068660248e-05, 4.938229210369754e-05, 8.299739795918411e-05, 0.00010380022972342312, 8.517231280276838e-05, 4.268909929422473e-05, 0.0001401656300703104, 9.411358034033013e-05, 2.686801426872722e-05, 6.495746686490732e-05, 0.0001003592975206599, 5.352049146764052e-05, 7.850467870218478e-05, 0.00010977598836417891, 4.14565932338694e-05, 3.5104888888888745e-05, 3.8687830439925495e-05, 5.4049993962081055e-05, 8.443534801969092e-05, 6.348045368620038e-05, 2.7965588866645727e-05, 8.024645161290204e-05, 7.902737072704074e-05, 5.711174287007689e-05, 6.703582151755061e-05, 8.883308144044379e-05, 7.213139693765705e-05, 6.373394531249959e-05, 3.6917399169773874e-05, 6.789261770645216e-05, 3.246629014083957e-05, 0.00010258354435651843, 7.079244034786678e-05, 4.494704706746724e-05, 5.506148760330608e-05, 5.142486134946193e-05, 3.6195156000000544e-05])

# Variances found for c = 1.5 at different points
variances /= max(variances)

plt.show()

# Plot values and their variances
for i, point in enumerate(points):
    color = colorsys.hls_to_rgb(variances[i], 0.5, 1.)
    plt.scatter(point[0], point[1], color = color)

def make_cmap(min_hue, max_hue):
    '''Creates a colormap'''
    colours = []
    for i in np.arange(min_hue, max_hue, 0.01):
        colours.append(colorsys.hls_to_rgb(i, 0.5, 1.))
    return(ListedColormap(colours))

norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
m = cm.ScalarMappable(cmap= make_cmap(0.5,1), norm=norm)
cbar = plt.colorbar(m)
cbar.set_label('Variance', rotation = 0)
cbar.set_clim(-2.0, 2.0)         
plt.grid()
plt.xlabel('Iterations')
plt.ylabel('Points')
plt.show()


