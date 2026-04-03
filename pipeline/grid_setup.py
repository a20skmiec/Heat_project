import numpy as np

### GRID SETUP


X, Y = np.meshgrid(np.arange(0, 7.55, 0.1), np.arange(0, 5.05, 0.1))
Nx = X.shape[1]
Ny = X.shape[0]
N = Nx * Ny

is_outerwall = np.isclose(X, 7) & (((Y > 0) & (Y < 1)) | ((Y > 4) & (Y < 5)))

is_neighborwall = np.isclose(Y, 0) | np.isclose(Y, 5) | np.isclose(X, 0)


is_innerwall = ((((Y > 2.95) & (Y < 3.15)) & ((X > 0) & (X < 1.5))) |
                (((X > 1.45) & (X < 1.65)) & ((Y > 3.5) & (Y < 5))) |
                (((X > 1.95) & (X < 2.10)) & ((Y > 0) & (Y < 3))) |
                (((X > 3.45) & (X < 3.65)) & ((Y > 3.45) & (Y < 5))) |
                (((X > 6.85) & (X < 7)) & (((Y > 0) & (Y < 1)) | ((Y > 4) & (Y < 5)) | ((Y > 0.95) & (Y < 4.05)))) |
                (((X > 3.45) & (X < 7)) & ((Y > 2.95) & (Y < 3.15))))

is_window = np.isclose(X, 7) & ((Y >= 1) & (Y <= 4))

is_radiator = ((((X > 0.45) & (X < 1.25)) & np.isclose(Y, 3.2)) |
               (((X < 6.65) & (X > 6.45)) & ((Y > 0.45) & (Y < 1.25))) |
               (((X < 6.65) & (X > 6.4)) & ((Y < 4.05) & (Y > 3.25))))


is_innerspace = ~(is_outerwall | is_neighborwall | is_innerwall | is_window | is_radiator)

print(np.sum(is_radiator))