from constats import MAX_PEOPLE_AT_STATION, MAX_PEOPLE_IN_TRAIN
from stations import Station, Train


class ModellingError(Exception):
    pass


class TooMuchPeopleAtTheStationError(ModellingError):
    pass


class TooMuchPeopleInTheTrainError(ModellingError):
    pass


async def check_station(station: Station):
    if len(station.people) > MAX_PEOPLE_AT_STATION:
        raise TooMuchPeopleAtTheStationError(f'Слишком много людей на станции {station}')


async def check_train(train: Train):
    if len(train.passengers) > MAX_PEOPLE_IN_TRAIN:
        raise TooMuchPeopleInTheTrainError('Слишком много людей в поезде')


if __name__ == '__main__':
    raise TooMuchPeopleInTheTrainError('Слишком много людей в поезде')
