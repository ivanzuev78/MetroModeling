import random

stationsName = ['Rokossovskaya', 'Sobornaya', 'Crystal', 'Zarechnaya', 'Pushkin library']
countOfStations = len(stationsName)
limitOfPeopleOnStation = 2000
maxPassengersInTrain = 400


class Station:
    def __init__(self):
        self.people = []
        self.is_train_to_go = False
        self.other_stations = None

    async def start_train(self):
        print('поезд запущен')

    async def arrivalOfPassengers(self):
        while True:
            for j in range(countOfStations):
                self.stations[j].append(Passenger(j))
                if len(self.stations[j]) >= 2000:
                    exit(f'На станции {stationsName[j]} слишком много людей')

    def init_other_stations(self, stations):
        self.other_stations = [s for s in stations if s is not self]


class Passenger:
    all_stations = []

    def __init__(self, station: Station):
        self.station_to_go = random.choice([s for s in self.all_stations if s is not station])
        station.people.append(self)


class Train:
    def __init__(self):
        self.station = 0
        self.passengers = []
        self.direction = 0  # 0 - right; 1 - left
        self.waiting = False


def generate_man(station):
    return Passenger(station)


async def create_man(station: Station):
    man = generate_man(station)
    # station.people.append(man)
