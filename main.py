import time
from asyncio import get_event_loop, gather, sleep
from typing import List

from about_async import my_func_async, my_func_coroutine
from check_funcs import check_station, check_train
from stations import create_man, Passenger, Station, STATIONS_NAME, Tunnel, generate_get_next_stations_func, Train

PASSENGER_START_GENERATION_TIME = 18 * 60
TIME_BETWEEN_STATIONS_MINUTES = [6, 3, 2, 7]

NUMB_OF_TRAINS = 10
SPEED = 100


async def modelling(numb_of_trains: int, stations_names: List[str], time_between_stations: List[int],
                    interval_between_trains: int):
    # some init
    if len(stations_names) != len(time_between_stations) + 1:
        raise ValueError('Не согласуются данные моделирования')
    get_next_stations = generate_get_next_stations_func(stations_names)

    stations = [Station(name) for name in stations_names]
    for station in stations:
        station.init_other_stations(stations)

    Passenger.all_stations = stations

    tunnels_left: List[Tunnel] = [Tunnel(time_tunnel) for time_tunnel in time_between_stations]
    tunnels_right: List[Tunnel] = [Tunnel(time_tunnel) for time_tunnel in time_between_stations]

    tunnels = tunnels_right + tunnels_left

    for station_index, tunnel in enumerate(tunnels_right):
        station_left = stations[station_index]
        station_right = stations[station_index + 1]

        station_left.right_tunnel = tunnel
        tunnel.end_station = station_right

    for station_index, tunnel in enumerate(tunnels_left):
        station_left = stations[station_index]
        station_right = stations[station_index + 1]

        station_right.left_tunnel = tunnel
        tunnel.end_station = station_left

    trains = [Train(get_next_stations) for _ in range(numb_of_trains)]
    trains_to_start = list(trains)

    modelling_time = 0
    statistics = []
    # save_statistics = my_func_coroutine()
    # save_statistics.send(None)
    while True:
        t = time.time()

        if modelling_time % interval_between_trains == 0 and trains_to_start:
            train = trains_to_start.pop(0)
            stations[0].get_train(train)

        modelling_time += 1

        if modelling_time >= PASSENGER_START_GENERATION_TIME:
            add_people_tasks = []
            for station in stations:
                add_people_tasks.append(create_man(station))

            await gather(*add_people_tasks)

        # for station in stations:
        #     debug_list = list(filter(lambda man: man.station_to_go == station.name, station.people))
        #     if debug_list:
        #         print('!!!')

        move_trains_in_tunnels_tasks = []
        for tunnel in tunnels:
            move_trains_in_tunnels_tasks.append(tunnel.move_trains())
        await gather(*move_trains_in_tunnels_tasks)

        move_trains_on_stations_tasks = []
        for station in stations:
            move_trains_on_stations_tasks.append(station.move_train())
        await gather(*move_trains_on_stations_tasks)

        check_list = []
        for station in stations:
            check_list.append(check_station(station))
        for train in trains:
            check_list.append(check_train(train))

        await gather(*check_list)

        duration_of_step_modelling = time.time() - t
        # print(modelling_time, duration_of_step_modelling)

        # await sleep((1 - duration_of_step_modelling) / SPEED)

        # print()
        # task_list = []
        # for station in stations:
        #     if station.is_train_to_go:
        #         task_list.append(station.start_train())
        #
        #
        if modelling_time % 60 == 0:
            print('=================')
            print(modelling_time)
            print(*[len(station.people) for station in stations])
            print('🚋')
            c = 0
            stat_1 = []
            for station in stations:
                stat_1.append(len(station.people))
            for i in range(len(stat_1)):
                c += stat_1[i]
            statistics.append(c // len(STATIONS_NAME))
            print(statistics[17:])
            # data = get_data(stations, trains)
            # statistics.append(data)
            # static = save_statistics.send(data)


def main():
    loop = get_event_loop()
    interval_between_trains = int(38 * 60 / NUMB_OF_TRAINS)
    time_between_stations = [t * 60 for t in TIME_BETWEEN_STATIONS_MINUTES]
    loop.run_until_complete(modelling(NUMB_OF_TRAINS, STATIONS_NAME, time_between_stations, interval_between_trains))


if __name__ == '__main__':
    main()
