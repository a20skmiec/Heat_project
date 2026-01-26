import numpy as np
from scipy.sparse import lil_array, csr_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

# siatka
X, Y = np.meshgrid(np.arange(0, 5.01, 0.1), np.arange(0, 4.01, 0.1))
Nx = X.shape[1]
Ny = X.shape[0]
N = Nx * Ny

# podział przestrzeni
is_outerwall = np.isclose(X, 0) & ((Y > 0) & (Y < 4))
is_neighborwall = np.isclose(Y, 4) | np.isclose(Y, 0)
is_innerwall = ((X >= 1.9) & (X <= 2.1)) & ((Y > 0) & (Y < 4))
is_window = np.isclose(X, 5) & ((Y > 0) & (Y < 4))
is_radiator = ((X >= 0.5) & (X <= 0.7)) & ((Y >= 1.9) & (Y <= 2.1))
is_innerspace = ~(is_outerwall | is_neighborwall | is_innerwall | is_window | is_radiator)

# Funkcja mapująca (i, j) -> indeks liniowy
def p(x, y):
    return x + y * Nx

def main_matrix(ht, hx, len_flat_vec, D_air, D_wall, l_wall, l_window, l_air):
    beta_wall = ((-l_wall/l_air) * ht) / hx
    beta_win = ((-l_window/l_air) * ht) / hx
    gamma_air = (D_air * ht) / (hx ** 2)
    gamma_wall = (D_wall * ht) / (hx ** 2)
    A = lil_array((N, N))
    for j in range(Ny):
        for i in range(Nx):
            row = p(i, j)
            # sciana zewnetrzna - war. Robina
            if is_outerwall[j, i]:
                A[row, row] = 3*gamma_air + 1 - gamma_air * hx * beta_wall
                A[row, p(i+1, j)], A[row, p(i, j-1)], A[row, p(i, j+1)] = -gamma_air, -gamma_air, -gamma_air

            # okno - war.Robina
            elif is_window[j, i]:
                A[row, row] = 3*gamma_air + 1 - gamma_air * hx * beta_win
                A[row, p(i-1, j)], A[row, p(i, j-1)], A[row, p(i, j+1)] = -gamma_air, -gamma_air, -gamma_air

            # sciana sasiada - dirichlet
            elif is_neighborwall[j, i]:
                A[row, row] = 1

            # wnetrze - klasyk
            elif is_innerspace[j, i] or is_radiator[j, i]:
                A[row, row] = 1 + 4*gamma_air
                A[row, p(i+1, j)], A[row, p(i-1, j)], A[row, p(i, j+1)], A[row, p(i, j-1)] = -gamma_air, -gamma_air, -gamma_air, -gamma_air

            # sciany miedzy pokojami - klasyk z inna dyfuzja
            elif is_innerwall[j, i]:
                A[row, row] = 1 + 4*gamma_wall
                A[row, p(i+1, j)], A[row, p(i-1, j)], A[row, p(i, j+1)], A[row, p(i, j-1)] = -gamma_wall, -gamma_wall, -gamma_wall, -gamma_wall
    return A



# A_csr = main_matrix(D_air, D_wall, ht, hx, N).tocsr()


def iteration_process(u0, sensor_point, ht, hx, T_max, len_flat_vec, D_air, D_wall, dest_temp, rad_power, dirichlet_temp, outside_temp, l_wall, l_window, l_air):
    A_csr = main_matrix(ht, hx, N, D_air, D_wall,  l_wall, l_window, l_air).tocsr()
    beta_wall = ((-l_wall / l_air) * ht) / hx
    beta_win = ((-l_window / l_air) * ht) / hx

    u = np.ones(N) * u0
    sensor_id = p(sensor_point[0], sensor_point[1])
    ts = np.arange(0, T_max + ht, ht)
    T_all = np.zeros((len(ts), len_flat_vec))
    T_all[0,] = u

    radiator_ids = np.where(is_radiator.flatten())[0]
    outwall_ids = np.where(is_outerwall.flatten())[0]
    window_ids = np.where(is_window.flatten())[0]
    neighbor_ids = np.where(is_neighborwall.flatten())[0]

    for t in range(1, len(ts)):
        # b na bazie poprzedniego kroku
        b = u.copy()

        # Grzejnik - termostat
        current_temp = u[sensor_id]
        if current_temp < dest_temp:
            b[radiator_ids] += rad_power * ht

        # Robin
        b[outwall_ids] += beta_wall * outside_temp
        b[window_ids] += beta_win * outside_temp

        # Dirichlet
        b[neighbor_ids] = dirichlet_temp

        # Rozwiązanie układu
        u = spsolve(A_csr, b)
        T_all[t] = u

    return T_all

# === Animacja ===
fig, ax = plt.subplots(figsize=(6, 5))
pcm = ax.pcolormesh(X, Y, T_all[0].reshape(Ny, Nx), shading='auto', cmap='jet', vmin=-5, vmax=30)
cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label("Temperatura [°C]")
ax.set_title("Symulacja ogrzewania")

def update(frame):
    pcm.set_array(T_all[frame].ravel())
    ax.set_title(f"Czas: {frame*ht:.0f}s, Czujnik: {T_all[frame][sensor_id]:.1f}°C")
    return pcm,

ani = animation.FuncAnimation(fig, update, frames=range(0, steps, 2), interval=50, blit=False)
plt.close()
HTML(ani.to_jshtml())