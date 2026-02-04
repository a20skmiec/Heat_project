from pipeline import grid_setup as grid
from scipy.sparse import lil_array

# Funkcja mapująca (i, j) -> liczba - indeks w splaszczonym wektrze
def p(x, y):
    return x + y * grid.Nx

# kosntrukcja macierzy dla układów równań - niejawne
# stricte macierzy - skłądniki które w iteracji są nzal od u
# np. dodane ciepło przez grzejnik
def main_matrix(ht, hx, len_flat_vec, D_air, D_wall, l_wall, l_window, l_air):
    beta_wall = ((-l_wall/l_air) * ht) / hx   # do warunku robina na scianie
    beta_win = ((-l_window/l_air) * ht) / hx   # do warunku robina na oknie
    gamma_air = (D_air * ht) / (hx ** 2)
    gamma_wall = (D_wall * ht) / (hx ** 2)
    A = lil_array((len_flat_vec, len_flat_vec))
    for j in range(grid.Ny):
        for i in range(grid.Nx):
            row = p(i, j)
            # sciana zewnetrzna - war. Robina
            if grid.is_outerwall[j, i]:
                A[row, row] = 3*gamma_air + 1 - gamma_air * hx * beta_wall
                A[row, p(i+1, j)], A[row, p(i, j-1)], A[row, p(i, j+1)] = -gamma_air, -gamma_air, -gamma_air

            # okno - war.Robina
            elif grid.is_window[j, i]:
                A[row, row] = 3*gamma_air + 1 - gamma_air * hx * beta_win
                A[row, p(i-1, j)], A[row, p(i, j-1)], A[row, p(i, j+1)] = -gamma_air, -gamma_air, -gamma_air

            # sciana sasiada - dirichlet
            elif grid.is_neighborwall[j, i]:
                A[row, row] = 1

            # wnetrze - klasyk
            elif grid.is_innerspace[j, i] or grid.is_radiator[j, i]:
                A[row, row] = 1 + 4*gamma_air
                A[row, p(i+1, j)], A[row, p(i-1, j)], A[row, p(i, j+1)], A[row, p(i, j-1)] = -gamma_air, -gamma_air, -gamma_air, -gamma_air

            # sciany miedzy pokojami - klasyk z inna dyfuzja
            elif grid.is_innerwall[j, i]:
                A[row, row] = 1 + 4*gamma_wall
                A[row, p(i+1, j)], A[row, p(i-1, j)], A[row, p(i, j+1)], A[row, p(i, j-1)] = -gamma_wall, -gamma_wall, -gamma_wall, -gamma_wall
    return A

