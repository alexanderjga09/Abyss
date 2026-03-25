def PerHour(mount, cycle_time, rsl=0, food=0):
    return (mount / (cycle_time * ((1.0 + (0.05 * (rsl + food))) ** -1))) * 3600
