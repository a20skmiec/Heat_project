import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML, display
import function as f
import grid_setup as grid

def anim(dane, results, html=False):
    Temp_min = results.min()
    Temp_max = results.max()
    fig, ax = plt.subplots(figsize=(8, 6))
    # Mapa kolorów
    pcm = ax.pcolormesh(grid.X, grid.Y, results[0].reshape(grid.Ny, grid.Nx),
                    shading='auto', cmap='inferno', vmin=Temp_min, vmax=Temp_max)

    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Temperatura ")
    ax.set_title("Symulacja ogrzewania")
    ax.set_aspect('equal')

    def update(frame):
        step_idx = frame * 20
        if step_idx >= len(results):
            step_idx = len(results) - 1

        current_T = results[step_idx]
        pcm.set_array(current_T.ravel())

        current_time = (step_idx) * dane['ht']
        temp_at_sensor = current_T[f.p(dane['sensor_pointx'], dane['sensor_pointy'])]

        ax.set_title(f"Czas: {current_time//60} h | Sensor: {temp_at_sensor:.1f}")
        return (pcm, )

    frames = len(results) // 20

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

    if html:
        display(HTML(ani.to_jshtml()))
    else:
        plt.show()

    return ani

