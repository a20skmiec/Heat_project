import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML, display
from pipeline import function as f
from pipeline import grid_setup as grid


# funkcja tworząca głowną animację zmiany ciepła na dwuwymiarowej siatce w zależnosci od czasu
def anim(dane, results, html=False):
    #Temp_min = results.min() - może użyje w pcm na vmin
    #Temp_max = results.max() - jak wyżej vmax
    fig, ax = plt.subplots(figsize=(8, 6))
    # Mapa kolorów
    pcm = ax.pcolormesh(grid.X, grid.Y, results[0].reshape(grid.Ny, grid.Nx),
                    shading='gouraud', cmap='inferno', vmin=-5, vmax=35)

    # pasek kolorów
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label("Temperatura ")

    ax.set_title("Symulacja ogrzewania")
    ax.set_aspect('equal')

    # aktualizacja klatek
    def update(frame):
        step_idx = frame * 10   # co 10 krok czasowy
        if step_idx >= len(results):
            step_idx = len(results) - 1

        # aktualny stan temp.
        current_T = results[step_idx]
        pcm.set_array(current_T.ravel())

        # aktualny czas sym.
        current_time = (step_idx) * dane['ht']

        # temp. w punkcie sensora
        temp_at_sensor = current_T[f.p(dane['sensor_pointx'], dane['sensor_pointy'])]

        # aktualizowany tytuł wykresu
        ax.set_title(f"Czas: {current_time//60} h | Sensor: {temp_at_sensor:.1f}")
        return (pcm, )

    # licz. klatek animacji
    frames = len(results) // 10

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

    # petla ktora wyswietla odpowiednio animacje w matplotlib lub ipynb html
    # w matplotlib brak paska pozwalającego na przesuwanie animacji samemu
    if html:
        html = ani.to_jshtml()
        plt.close(fig)
        display(HTML(html))
    else:
        plt.show()

    return ani

