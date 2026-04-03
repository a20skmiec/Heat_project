import numpy as np
from pipeline import function as f
from pipeline import grid_setup as grid
from scipy.sparse.linalg import spsolve


# Iteration
def iteration_process(u0, sensor_point, ht, hx, T_max, len_flat_vec, D_air, D_wall, dest_temp,
                      dirichlet_temp, outside_temp, l_wall, l_window, l_air, rad_power, r, pressure, V, c):

    A_csr = f.main_matrix(ht, hx, grid.N, D_air, D_wall, l_wall, l_window, l_air, rad_power, r, pressure, V, c).tocsr()
    A_csr_rad = f.main_matrix(ht, hx, grid.N, D_air, D_wall, l_wall, l_window, l_air, rad_power, r, pressure, V, c, rad_use=True).tocsr()

    beta_wall = ((-l_wall / l_air) * ht) / hx
    beta_win = ((-l_window / l_air) * ht) / hx

    u = np.ones(grid.N) * u0
    sensor_id = f.p(sensor_point[0], sensor_point[1])   # sensor
    ts = np.arange(0, T_max + ht, ht)
    T_all = np.zeros((len(ts), len_flat_vec))
    T_all[0,] = u

    outwall_ids = np.where(grid.is_outerwall.flatten())[0]
    window_ids = np.where(grid.is_window.flatten())[0]
    neighbor_ids = np.where(grid.is_neighborwall.flatten())[0]

    for t in range(1, len(ts)):
        b = u.copy()

        # boundary robin
        b[outwall_ids] -= beta_wall * outside_temp
        b[window_ids] -= beta_win * outside_temp

        # Dirichlet
        b[neighbor_ids] = dirichlet_temp

        # Radiator with the simplest termostat
        current_temp = u[sensor_id]

        if current_temp < dest_temp:
            u = spsolve(A_csr_rad, b)
            T_all[t] = u
        else:
            u = spsolve(A_csr, b)
            T_all[t] = u

    return T_all