import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

plt.rcParams.update({"font.size": 10})

N = [11, 23, 32, 71, 101, 225, 317]

df_rand_var = pd.read_csv("variance_rand.txt", names=["N", "Var"])
df_rand_mean = pd.read_csv("mean_rand.txt", names=["N", "Mean"])

df_lhs_var = pd.read_csv("variance_lhs.txt", names=["N", "Var"])
df_lhs_mean = pd.read_csv("mean_lhs.txt", names=["N", "Mean"])

df_ortho_var = pd.read_csv("variance_ortho.txt", names=["N", "Var"])
df_ortho_mean = pd.read_csv("mean_ortho.txt", names=["N", "Mean"])

df_control_var = pd.read_csv("variance_control2.txt", names=["N", "Var"])
df_control_mean = pd.read_csv("mean_control2.txt", names=["N", "Mean"])

x_data = np.array(N) ** 2

comboX = np.append(x_data, x_data)
comboX = np.append(comboX, x_data)
comboX = np.append(comboX, x_data)

mean_var_ortho = []
mean_var_lhs = []
mean_var_rand = []
mean_var_cont = []

sigma_ortho = []
sigma_lhs = []
sigma_rand = []
sigma_cont = []

for n in N:

    column_ortho = df_ortho_var.loc[df_ortho_var["N"].isin([n])]
    column_lhs = df_lhs_var.loc[df_lhs_var["N"].isin([n])]
    column_rand = df_rand_var.loc[df_rand_var["N"].isin([n])]
    column_cont = df_control_var.loc[df_control_var["N"].isin([n])]

    sig_o = column_ortho["Var"].std(axis=0)
    sig_l = column_lhs["Var"].std(axis=0)
    sig_r = column_rand["Var"].std(axis=0)
    sig_c = column_cont["Var"].std(axis=0)

    mean_o = column_ortho["Var"].mean(axis=0)
    mean_l = column_lhs["Var"].mean(axis=0)
    mean_r = column_rand["Var"].mean(axis=0)
    mean_c = column_cont["Var"].mean(axis=0)

    sigma_ortho.append(sig_o)
    sigma_lhs.append(sig_l)
    sigma_rand.append(sig_r)
    sigma_cont.append(sig_c)

    mean_var_ortho.append(mean_o)
    mean_var_lhs.append(mean_l)
    mean_var_rand.append(mean_r)
    mean_var_cont.append(mean_c)

y1 = mean_var_ortho
y2 = mean_var_lhs
y3 = mean_var_rand
y4 = mean_var_cont

comboY = np.append(y1, y2)
comboY = np.append(comboY, y3)
comboY = np.append(comboY, y4)
comboSig = np.append(sigma_ortho, sigma_lhs)
comboSig = np.append(comboSig, sigma_rand)
comboSig = np.append(comboSig, sigma_cont)


def func1(x, q1, q2, q3, q4, c, d):
    return q1 / x ** d + c


def func2(x, q1, q2, q3, q4, c, d):
    return q2 / x ** d + c


def func3(x, q1, q2, q3, q4, c, d):
    return q3 / x ** d + c


def func4(x, q1, q2, q3, q4, c, d):
    return q4 / x ** d + c


def comboFunc(comboData, q1, q2, q3, q4, c, d):
    # single data set passed in, extract separate data
    extract1 = comboData[: len(y1)]  # first data
    extract2 = comboData[len(y2) : len(y1) + len(y2)]  # second data
    extract3 = comboData[len(y1) + len(y2) : len(y1) + len(y2) + len(y3)]
    extract4 = comboData[len(y1) + len(y2) + len(y3) :]

    result1 = func1(extract1, q1, q2, q3, q4, c, d)
    result2 = func2(extract2, q1, q2, q3, q4, c, d)
    result3 = func3(extract3, q1, q2, q3, q4, c, d)
    result4 = func4(extract4, q1, q2, q3, q4, c, d)

    res = np.append(result1, result2)
    res = np.append(res, result3)
    res = np.append(res, result4)
    return res


fittedParameters, pcov = curve_fit(
    comboFunc,
    comboX,
    comboY,
    sigma=5 * comboSig,
    p0=[1, 1, 1, 1, 1, 1.2],
    bounds=(0, [np.inf, np.inf, np.inf, np.inf, np.inf, 1.3]),
)
plt.errorbar(x_data, mean_var_lhs, yerr=6 * np.array(sigma_lhs), fmt="ro", label="LHS")
plt.errorbar(
    x_data,
    mean_var_ortho,
    yerr=6 * np.array(sigma_ortho),
    fmt="bo",
    label="Orthogonal",
)
plt.errorbar(
    x_data, mean_var_rand, yerr=6 * np.array(sigma_rand), fmt="go", label="Random"
)
plt.errorbar(
    x_data, mean_var_cont, yerr=6 * np.array(sigma_cont), fmt="mo", label="Control"
)

q1, q2, q3, q4, c, d = fittedParameters

a_lo = q2 ** (1 / d) / q1 ** (1 / d)
a_ro = q3 ** (1 / d) / q1 ** (1 / d)
a_cr = q3 ** (1 / d) / q4 ** (1 / d)

y_fit_1 = func1(x_data, q1, q2, q3, q4, c, d)
y_fit_2 = func2(x_data, q1, q2, q3, q4, c, d)
y_fit_3 = func3(x_data, q1, q2, q3, q4, c, d)
y_fit_4 = func4(x_data, q1, q2, q3, q4, c, d)

plt.plot(
    x_data, y_fit_2, "r-", label=r"$q_{LHS}$" + "=%5.3f, d=%5.3f" % (q2, d),
)  # plot the equation using the fitted parameters
plt.plot(
    x_data, y_fit_1, "b-", label=r"$q_{Ortho}$" + "=%5.3f, d=%5.3f" % (q1, d),
)  # plot the equation using the fitted parameters
plt.plot(
    x_data, y_fit_3, "g-", label=r"$q_{Rand}$" + "=%5.3f, d=%5.3f" % (q3, d),
)
plt.plot(
    x_data, y_fit_4, "m-", label=r"$q_{Cont}$" + "=%5.3f, d=%5.3f" % (q4, d),
)
plt.hlines(
    0.0006,
    1418,
    20149,
    linestyles="--",
    colors="orangered",
    label=r"$\alpha_{LHS,Ortho} =$" + str(round(a_lo, 2)),
)
plt.hlines(
    0.0009,
    977,
    24000,
    linestyles="--",
    colors="magenta",
    label=r"$\alpha_{Rand,Ortho} =$" + str(round(a_ro, 2)),
)
plt.hlines(
    0.001,
    19655,
    21000,
    linestyles="--",
    colors="purple",
    label=r"$\alpha_{Rand,Cont} =$" + str(round(a_cr, 2)),
)

plt.xlabel("N")
plt.ylabel(r"$\frac{\sigma}{\barx}$")
plt.yscale("log")
plt.xscale("log")
plt.title("Acceleration factor")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1), ncol=1, fancybox=True, shadow=True)
plt.savefig("vars.png", bbox_inches="tight")
plt.show()
