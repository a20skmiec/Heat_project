import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import function as f

# PARAMETRY
# Kroki czasowe i przestrzenne
hx = 0.1
ht = 1
T_max = 3600
# Lambda
l_air = 0.026
l_wall = 1.0
l_window = 0.8
# DYFUZJE
D_air = 1.9e-5 * 1000
D_wall = 5.0e-7 * 500
# temp.
outside_temp = -5.0
dirichlet_temp = 20.0
u0 = 15.0
dest_temp = 22.0
# Grzejnik
rad_power = 100.0
# Sensor
sensor_point = (30, 25)

#URUCHOMIENIE
results = f.iteration_process(
    u0=u0,
    sensor_point=sensor_point,
    ht=ht,
    hx=hx,
    T_max=T_max,
    len_flat_vec=f.N,
    D_air=D_air,
    D_wall=D_wall,
    dest_temp=dest_temp,
    rad_power=rad_power,
    dirichlet_temp=dirichlet_temp,
    outside_temp=outside_temp,
    l_wall=l_wall,
    l_window=l_window,
    l_air=l_air
)

print(f"Symulacja zakończona. Liczba kroków: {results.shape[0]}")
print(f"Temperatura końcowa na czujniku: {results[-1, f.p(sensor_point[0], sensor_point[1])]:.2f} °C")


# ANIMACJA
fig, ax = plt.subplots(figsize=(8, 6))

# Mapa kolorów
pcm = ax.pcolormesh(f.X, f.Y, results[0].reshape(f.Ny, f.Nx),
                    shading='auto', cmap='inferno', vmin=-5, vmax=30)

cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label("Temperatura [°C]")
ax.set_title("Symulacja ogrzewania")
ax.set_aspect('equal')


def update(frame):
    step_idx = frame * 10
    if step_idx >= len(results):
        step_idx = len(results) - 1

    current_T = results[step_idx]
    pcm.set_array(current_T.ravel())

    current_time = step_idx * ht
    temp_at_sensor = current_T[f.p(sensor_point[0], sensor_point[1])]

    ax.set_title(f"Czas: {current_time / 60:.1f} min | Sensor: {temp_at_sensor:.1f}°C")
    return pcm,

# klatki

frames = len(results) // 10

ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

print("Gnerowanie animacji ... ")
html_content = ani.to_jshtml()
with open("symulacja.html", "w", encoding='utf-8') as g:
    g.write(html_content)
print("Gotowe! Otwórz plik 'symulacja.html'.")

#plt.close()
#HTML(ani.to_jshtml())
# ... (kod animacji)

#print("Generowanie pliku GIF... to może chwilę potrwać.")
# Zapisz do pliku w folderze projektu
#ani.save("symulacja.gif", writer='pillow', fps=20)
#print("Gotowe! Otwórz plik symulacja.gif w folderze projektu.")