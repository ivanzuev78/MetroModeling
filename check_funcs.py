from typing import List

from stations import Station, Train, MAX_PEOPLE_AT_STATION, MAX_PEOPLE_IN_TRAIN


class TooMuchPeopleAtTheStationError(Exception):
    pass

class TooMuchPeopleInTheTrainError(Exception):
    pass


async def check_station(station: Station):
    if len(station.people) > MAX_PEOPLE_AT_STATION:
        raise TooMuchPeopleAtTheStationError(f'Слишком много людей на станции {station}')


async def check_train(train: Train):
    if len(train.passengers) > MAX_PEOPLE_IN_TRAIN:
        raise TooMuchPeopleInTheTrainError('Слишком много людей в поезде')


if __name__ == '__main__':
    raise TooMuchPeopleInTheTrainError('Слишком много людей в поезде')