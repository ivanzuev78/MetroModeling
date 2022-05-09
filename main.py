import datetime
import os
import time
from asyncio import get_event_loop, gather
from typing import List
import signal

from check_funcs import check_station, check_train
from constats import SPEED, PASSENGER_START_GENERATION_TIME, NUMB_OF_TRAINS, TIME_BETWEEN_STATIONS_MINUTES, \
    STAT_GET_INTERVAL, STATIONS_NAME
from statist import Statistics, show_statistics
from stations import create_man, Passenger, Station, Tunnel, generate_get_next_stations_func, Train


async def modelling(numb_of_trains: int, stations_names: List[str], time_between_stations: List[int],
                    interval_between_trains: int, statistics_watcher: Statistics):
    time_for_step = 1 / SPEED
    start_time = datetime.time(12)
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

    for station_index, tunnel_right in enumerate(tunnels_right):
        station_left = stations[station_index]
        station_right = stations[station_index + 1]

        station_left.right_tunnel = tunnel_right
        tunnel_right.end_station = station_right

    for station_index, tunnel_right in enumerate(tunnels_left):
        station_left = stations[station_index]
        station_right = stations[station_index + 1]

        station_right.left_tunnel = tunnel_right
        tunnel_right.end_station = station_left

    trains = [Train(get_next_stations, statistics_watcher) for _ in range(numb_of_trains)]
    trains_to_start = list(trains)

    modelling_time = 0
    statistics_watcher.stations = stations
    statistics_watcher.trains = trains
    # save_statistics = my_func_coroutine()
    # save_statistics.send(None)
    while True:
        t = time.time()

        if modelling_time % interval_between_trains == 0 and trains_to_start:
            train = trains_to_start.pop(0)
            train.next_station = stations[0]
            stations[0].get_train(train)

        modelling_time += 1

        if modelling_time >= PASSENGER_START_GENERATION_TIME:
            add_people_tasks = []
            for station in stations:
                add_people_tasks.append(create_man(station))

            await gather(*add_people_tasks)

        for station in stations:
            debug_list = list(filter(lambda man: man.station_to_go == station.name, station.people))
            if debug_list:
                print('!!!')

        move_trains_in_tunnels_tasks = []
        for tunnel_right in tunnels:
            move_trains_in_tunnels_tasks.append(tunnel_right.move_trains())
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

        # if time_for_step > duration_of_step_modelling and modelling_time % 2 == 0:
        #     time.sleep(time_for_step - duration_of_step_modelling)


        if modelling_time % STAT_GET_INTERVAL == 0:
            os.system('cls||clear')


            for tunnel_right, tunnel_left, station in zip(tunnels_right, tunnels_left, stations):

                # Печать станций
                train_at_station = ''
                if station.train_at_station:
                    train_at_station = f' [{len(station.train_at_station.passengers)}] '
                print(station, len(station.people), train_at_station)

                # Печать путей
                lines_right = tunnel_right.get_print_lines()
                lines_left = tunnel_left.get_print_lines(True)
                for line_right, line_left in zip(lines_right, lines_left):
                    print(line_right + line_left)

            # Печать последней станции
            station = stations[-1]
            train_at_station = ''
            if station.train_at_station:
                train_at_station = f' [{len(station.train_at_station.passengers)}] '
            print(station, len(station.people), train_at_station)

            # Сбор статистики
            statistics_tasks = []
            for statistics_object in stations + trains:
                statistics_tasks.append(statistics_object.remember_stats())
            await gather(*statistics_tasks)
            print(statistics_watcher.current_step)
            statistics_watcher.current_step += 1
            # time.sleep(0.1)


def termination_handler_creator(statistics):
    def termination_handler(*args, **kwargs):
        os.system('cls||clear')
        show_statistics(statistics)
        exit()

    return termination_handler


def main():
    statistics_watcher = Statistics()
    termination_handler = termination_handler_creator(statistics_watcher)
    signal.signal(signal.SIGINT, termination_handler)
    loop = get_event_loop()
    interval_between_trains = int(38 * 60 / NUMB_OF_TRAINS)
    time_between_stations = [t * 60 for t in TIME_BETWEEN_STATIONS_MINUTES]
    try:
        loop.run_until_complete(
            modelling(NUMB_OF_TRAINS, STATIONS_NAME, time_between_stations, interval_between_trains, statistics_watcher))
    except:
        termination_handler()

if __name__ == '__main__':
    main()
