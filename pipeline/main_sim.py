import function as f
import iteration as i
import json
import grid_setup as grid
from pathlib import Path


def read(file):
    with open(file, 'r') as h:
        data = json.load(h)
    return data

# URUCHOMIENIE
def wyniki(file):
    with open(file, 'r') as g:
        data = json.load(g)

    return i.iteration_process(
        u0=data['u0'],
        sensor_point=(data['sensor_pointx'], data['sensor_pointy']),
        ht=data['ht'],
        hx=data['hx'],
        T_max=data['T_max'],
        len_flat_vec=grid.N,
        D_air=data['D_air'],
        D_wall=data['D_wall'],
        dest_temp=data['dest_temp'],
        rad_power=data['rad_power'],
        dirichlet_temp=data['dirichlet_temp'],
        outside_temp=data['outside_temp'],
        l_wall=data['l_wall'],
        l_window=data['l_window'],
        l_air=data['l_air'])


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "dane.json"

dane = read(DATA_FILE)
results = wyniki(DATA_FILE)