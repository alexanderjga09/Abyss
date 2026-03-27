from numba import njit


@njit
def PerHour(mount, cycle_time, rsl=0, feed=0):
    return (mount / (cycle_time * ((1.0 + (0.05 * (rsl + feed))) ** -1))) * 3600
