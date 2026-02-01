import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import function as f
import json


def read(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

# URUCHOMIENIE
def wyniki(file):
    with open(file, 'r') as g:
        data = json.load(g)

    return f.iteration_process(
        u0=data['u0'],
        sensor_point=(data['sensor_pointx'], data['sensor_pointy']),
        ht=data['ht'],
        hx=data['hx'],
        T_max=data['T_max'],
        len_flat_vec=f.N,
        D_air=data['D_air'],
        D_wall=data['D_wall'],
        dest_temp=data['dest_temp'],
        rad_power=data['rad_power'],
        dirichlet_temp=data['dirichlet_temp'],
        outside_temp=data['outside_temp'],
        l_wall=data['l_wall'],
        l_window=data['l_window'],
        l_air=data['l_air'])

dane = read('data/dane.json')
results = wyniki('data/dane.json')

# ANIMACJA
fig, ax = plt.subplots(figsize=(8, 6))

# Mapa kolorów
pcm = ax.pcolormesh(f.X, f.Y, results[0].reshape(f.Ny, f.Nx),
                    shading='auto', cmap='inferno', vmin=-5, vmax=35)
print(results[0].min())

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

    current_time = step_idx * dane['ht']
    temp_at_sensor = current_T[f.p(dane['sensor_pointx'], dane['sensor_pointy'])]

    ax.set_title(f"Czas: {current_time//60} min | Sensor: {temp_at_sensor:.1f}°C")
    return pcm,


frames = len(results) // 10

ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

print("Gnerowanie animacji ... ")
html_content = ani.to_jshtml()
with open("symulacja.html", "w", encoding='utf-8') as g:
    g.write(html_content)
print("Gotowe otwórz symulacja.html")
