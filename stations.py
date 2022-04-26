import random


class Station:
    def __init__(self):
        self.people = []
        self.is_train_to_go = False
        self.other_stations = None

    async def start_train(self):
        print('поезд запущен')

    async def generate_man(self):
        pass

    def init_other_stations(self, stations):
        self.other_stations = [s for s in stations if s is not self]


class Passenger:
    all_stations = []

    def __init__(self, station: Station):
        self.station_to_go = random.choice([s for s in self.all_stations if s is not station])
        station.people.append(self)


class Train:
    def __init__(self):
        pass


def generate_man(station):
    return Passenger(station)


async def create_man(station: Station):
    man = generate_man(station)
    # station.people.append(man)
