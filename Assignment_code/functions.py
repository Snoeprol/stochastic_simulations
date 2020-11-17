def Zn_1(z_n, c):
    """Calculates next step for 
    a candidate in Mandelbrot set"""
    return z_n ** 2 + c


def sim(c1, c2, lim):
    converger = 0
    z = 0
    c = complex(c1, c2)

    while converger < lim:
        z_n1 = Zn_1(z, c)

        if abs(z_n1) < 2:
            z = z_n1
            converger += 1

        else:
            return (False, c)

    return (True, c)
