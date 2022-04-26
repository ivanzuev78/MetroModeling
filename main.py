from asyncio import get_event_loop, gather

from about_async import my_func_async, my_func_coroutine
from stations import create_man, Passenger


async def modelling():
    # some init
    stations = []
    for station in stations:
        station.init_other_stations(stations)
    Passenger.all_stations = stations
    trains = []
    my_time = 0
    statistics = []
    save_statistics = my_func_coroutine()
    save_statistics.send(None)
    while True:
        my_time += 1
        add_people_tasks = []
        for station in stations:
            add_people_tasks.append(create_man(station))

        await gather(add_people_tasks)


        # task_list = []
        # for station in stations:
        #     if station.is_train_to_go:
        #         task_list.append(station.start_train())
        #
        #
        # if my_time % 60 == 0:
        #     data = get_data(stations, trains)
        #     statistics.append(data)
        #     static = save_statistics.send(data)
        #

def main():
    loop = get_event_loop()
    loop.run_until_complete(modelling())



if __name__ == '__main__':
    main()