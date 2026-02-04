import numpy as np

# siatka
X, Y = np.meshgrid(np.arange(0, 7.55, 0.05), np.arange(0, 5.05, 0.05))
Nx = X.shape[1]
Ny = X.shape[0]
N = Nx * Ny

# podział przestrzeni
is_outerwall = np.isclose(X, 7) & (((Y > 0) & (Y < 1)) | ((Y > 4) & (Y < 5)))

is_neighborwall = np.isclose(Y, 0) | np.isclose(Y, 5) | np.isclose(X, 0)

is_innerwall = ((((Y > 2.95) & (Y < 3.15)) & ((X > 0) & (X < 1.5))) |
                (((X > 1.45) & (X < 1.65)) & ((Y > 3.5) & (Y < 5))) |
                (((X > 1.95) & (X < 2.10)) & ((Y > 0) & (Y < 3))) |
                (((X > 3.45) & (X < 3.65)) & ((Y > 3.45) & (Y < 5))) |
                (((X > 6.85) & (X < 7)) & (((Y > 0) & (Y < 1)) | ((Y > 4) & (Y < 5)))) |
                (((X > 3.45) & (X < 7)) & ((Y > 2.95) & (Y < 3.15))))

is_window = np.isclose(X, 7) & ((Y >= 1) & (Y <= 4))

is_radiator = ((((X > 0.45) & (X < 1.25)) & np.isclose(Y, 3.2)) |
               (((X <= 6.75) & (X > 6.60)) & ((Y > 0.50) & (Y < 1.2))) |
               (((X <= 6.60) & (X > 6.4)) & ((Y < 4) & (Y > 3.3))))

is_innerspace = ~(is_outerwall | is_neighborwall | is_innerwall | is_window | is_radiator)
