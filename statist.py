from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

GRAPHICS_PATH = Path('graphics')
GRAPHICS_STATIONS_PATH = Path('stations')
GRAPHICS_TRAINS_PATH = Path('trains')


class Statistics:

    def __init__(self):
        self.stations = []
        self.trains = []
        self.travel_times = defaultdict(list)
        self.current_step = 0

    def add_travel_time(self, travel_time):
        self.travel_times[self.current_step].append(travel_time)


def create_graphs(statistics: Statistics):
    generate_stations_graphs(statistics)
    generate_train_graphs(statistics)
    generate_average_travel_time_graph(statistics)


def generate_stations_graphs(statistics: Statistics):
    for station in statistics.stations:
        y = station.statistics
        x = [i for i in range(len(station.statistics))]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set(xlabel='time (min)', ylabel='Количество людей на станции',
               title=f'{station}')
        ax.grid()

        fig.savefig(GRAPHICS_PATH / GRAPHICS_STATIONS_PATH / f"{station}.png")

        plt.close(fig)


def generate_train_graphs(statistics: Statistics):
    for train_numb, train in enumerate(statistics.trains):
        y = train.statistics
        x = [i for i in range(len(train.statistics))]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set(xlabel='time (min)', ylabel=f'Количество людей в поезде',
               title=f'Поезд № {train.train_number}')
        ax.grid()

        fig.savefig(GRAPHICS_PATH / GRAPHICS_TRAINS_PATH / f"train_{train.train_number}.png")
        plt.close(fig)


def generate_average_travel_time_graph(statistics: Statistics):
    steps = []
    travel_times = []
    for step, travel_time in statistics.travel_times.items():
        steps.append(step)
        travel_times.append(round(sum(travel_time) / len(travel_time), 2))

    fig, ax = plt.subplots()
    ax.plot(steps, travel_times)

    ax.set(xlabel='time (min)', ylabel=f'Количество людей в поезде',
           title=f'Среднее время поездки')
    ax.grid()
    fig.savefig(GRAPHICS_PATH / f"average_travel_time.png")

    plt.show()
