from pipeline import grid_setup as grid
from scipy.sparse import lil_array

# flattening function
def p(x, y):
    return x + y * grid.Nx

# main matri constructin
def main_matrix(ht, hx, len_flat_vec, D_air, D_wall, l_wall, l_window, l_air, rad_power, r, pressure, V, c, rad_use=False):
    rad_coef = (rad_power * r) / (pressure * V * c)
    beta_wall = ((-l_wall/l_air) * ht) / hx
    beta_win = ((-l_window/l_air) * ht) / hx
    gamma_air = (D_air * ht) / (hx ** 2)
    gamma_wall = (D_wall * ht) / (hx ** 2)
    A = lil_array((len_flat_vec, len_flat_vec))
    for j in range(grid.Ny):
        for i in range(grid.Nx):
            row = p(i, j)
            # =outerwall - Robin boundary condition
            if grid.is_outerwall[j, i]:
                A[row, row] = 3*gamma_air + 1 - gamma_air * hx * beta_wall
                A[row, p(i+1, j)], A[row, p(i, j-1)], A[row, p(i, j+1)] = -gamma_air, -gamma_air, -gamma_air

            # window - Robin's boundary condition
            elif grid.is_window[j, i]:
                A[row, row] = 3*gamma_air + 1 - gamma_air * hx * beta_win
                A[row, p(i-1, j)], A[row, p(i, j-1)], A[row, p(i, j+1)] = -gamma_air, -gamma_air, -gamma_air

            # neighbor wall - constant temp. - Dirichlet
            elif grid.is_neighborwall[j, i]:
                A[row, row] = 1

            # radiator
            elif grid.is_radiator[j, i]:
                if rad_use:
                    A[row, row] = 1 + 4 * gamma_air - ht * rad_coef
                    A[row, p(i + 1, j)], A[row, p(i - 1, j)], A[row, p(i, j + 1)], A[row, p(i, j - 1)] = -gamma_air, -gamma_air, -gamma_air, -gamma_air
                else:
                    A[row, row] = 1 + 4 * gamma_air
                    A[row, p(i + 1, j)], A[row, p(i - 1, j)], A[row, p(i, j + 1)], A[row, p(i, j - 1)] = -gamma_air, -gamma_air, -gamma_air, -gamma_air

            # innerspace- classic model
            elif grid.is_innerspace[j, i]:
                A[row, row] = 1 + 4*gamma_air
                A[row, p(i+1, j)], A[row, p(i-1, j)], A[row, p(i, j+1)], A[row, p(i, j-1)] = -gamma_air, -gamma_air, -gamma_air, -gamma_air

            # walls beetwen rooms - different diffusion
            elif grid.is_innerwall[j, i]:
                A[row, row] = 1 + 4*gamma_wall
                A[row, p(i+1, j)], A[row, p(i-1, j)], A[row, p(i, j+1)], A[row, p(i, j-1)] = -gamma_wall, -gamma_wall, -gamma_wall, -gamma_wall
    return A

