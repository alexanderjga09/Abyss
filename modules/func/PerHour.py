def PerHour(mount, cycle_time, rsl=0):
    return (mount / (cycle_time * ((1.0 + (0.05 * rsl)) ** -1))) * 3600
