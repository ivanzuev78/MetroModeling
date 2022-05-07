import random
from typing import List, Callable

STATIONS_NAME = ['Rokossovskaya', 'Sobornaya', 'Crystal', 'Zarechnaya', 'Pushkin library']
TIME_AT_STATION = 15
MAX_PEOPLE_AT_STATION = 1000
MAX_PEOPLE_IN_TRAIN = 400

def generate_get_next_stations_func(stations):

    def get_next_stations(current_station: str, direction: int):
        current_station_index = stations.index(current_station)
        return stations[current_station_index + direction::direction]

    return get_next_stations


class Station:
    right_tunnel: "Tunnel"
    left_tunnel: "Tunnel"
    train_at_station: "Train"

    def __init__(self, name: str):
        self.name = name
        self.people = []  # type: List[Passenger]
        self.other_stations = None
        self.train_at_station = None
        self.right_tunnel = None
        self.left_tunnel = None

    def init_other_stations(self, stations):
        self.other_stations = [s for s in stations if s is not self]

    def send_train(self):


        # Обработка крайнего правого туннеля
        if self.right_tunnel is None:
            self.train_at_station.direction = -1
            self.left_tunnel.get_train(self.train_at_station)

        # Обработка левого правого туннеля
        elif self.left_tunnel is None:
            self.train_at_station.direction = 1
            self.right_tunnel.get_train(self.train_at_station)

        # Отправка поезда в правый туннель
        elif self.train_at_station.direction == 1:
            self.right_tunnel.get_train(self.train_at_station)

        # Отправка поезда в левый туннель
        elif self.train_at_station.direction == -1:
            self.left_tunnel.get_train(self.train_at_station)

        self.train_at_station.get_passengers(self)
        self.train_at_station = None

    def get_train(self, train: "Train"):
        self.train_at_station = train
        train.current_time = 0
        train.drop_passengers_off(self)

    async def move_train(self):
        if self.train_at_station:
            self.train_at_station.current_time += 1

            if self.train_at_station.current_time == TIME_AT_STATION:
                self.send_train()

    def __str__(self):
        return self.name


class Train:
    def __init__(self, get_next_stations: Callable):
        self.passengers = []
        self.direction = 1  # 1 - right; -1 - left
        self.current_time = 0
        self.get_next_stations = get_next_stations

    def drop_passengers_off(self, station: Station):
        passengers_to_drop = list(
            filter(lambda passenger: station.name == passenger.station_to_go, self.passengers))

        for passenger in passengers_to_drop:
            self.passengers.remove(passenger)
            del passenger

    def get_passengers(self, station: Station):
        next_stations = self.get_next_stations(station.name, self.direction)
        passengers_to_get = []

        for passenger in station.people:
            if len(self.passengers + passengers_to_get) >= MAX_PEOPLE_IN_TRAIN:
                break
            if passenger.station_to_go in next_stations:
                passengers_to_get.append(passenger)

        for passenger in passengers_to_get:
            station.people.remove(passenger)
            self.passengers.append(passenger)


class Tunnel:
    trains: List[Train]

    def __init__(self, time_len: int):
        self.time_len = time_len
        self.end_station = None
        self.trains = []

    def get_train(self, train: Train):
        train.current_time = 0
        self.trains.append(train)

    def send_train(self, train: Train):
        self.trains.remove(train)
        self.end_station.get_train(train)

    async def move_trains(self):
        train_to_send = None
        for train in self.trains:
            train.current_time += 1
            if train.current_time == self.time_len:
                train_to_send = train

        if train_to_send:
            self.send_train(train_to_send)


class Passenger:
    all_stations = []

    def __init__(self, station: Station):
        self.station_to_go = random.choice([s.name for s in self.all_stations if s is not station])
        station.people.append(self)


def generate_man(station):
    return Passenger(station)


async def create_man(station: Station):
    man = generate_man(station)
    # station.people.append(man)


if __name__ == '__main__':
    line_1 = ['Rokossovskaya', 'Sobornaya', 'Crystal', 'Zarechnaya', 'Pushkin library']
    line_2 = ['111', '222', '333', '444', '555']
    get_next_stations_line_1 = generate_get_next_stations_func(line_1)
    get_next_stations_line_2 = generate_get_next_stations_func(line_2)
    # ['Rokossovskaya', 'Sobornaya', 'Crystal', 'Zarechnaya', 'Pushkin library']

    print(get_next_stations_line_1('Crystal', -1))
    print(get_next_stations_line_2('555', -1))

    # 398 399 400
    #      0   1   2   3   4
    #
    station = Station('my station debug')
    print(str(station))

