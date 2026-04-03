import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML, display
from pipeline import function as f
from pipeline import grid_setup as grid
from main_sim import dane, results

# Animation of the heat transfer - run in the end
def anim(dane, results, html=False):
    fig, ax = plt.subplots(figsize=(8, 6))
    pcm = ax.pcolormesh(grid.X, grid.Y, results[0].reshape(grid.Ny, grid.Nx),
                    shading='gouraud', cmap='inferno', vmin=-5, vmax=35)

    # colorbar
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Temperatura ")

    ax.set_title("Symulacja ogrzewania")
    ax.set_aspect('equal')

    # frame update
    def update(frame):
        step_idx = frame * 10   # co 10 krok czasowy
        if step_idx >= len(results):
            step_idx = len(results) - 1

        # actual temp
        current_T = results[step_idx]
        pcm.set_array(current_T.ravel())

        # sim time
        current_time = (step_idx) * dane['ht']

        # sensor
        temp_at_sensor = current_T[f.p(dane['sensor_pointx'], dane['sensor_pointy'])]

        # dynamic title
        ax.set_title(f"Czas: {current_time//60} h | Sensor: {temp_at_sensor:.1f}")
        return (pcm, )

    # frames
    frames = len(results) // 10

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

    if html:
        ht = ani.to_jshtml()
        plt.close(fig)
        display(HTML(ht))
    else:
        plt.show()

    return ani


if __name__ == "__main__":
    anim(dane, results)

