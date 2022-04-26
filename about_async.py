from asyncio import get_event_loop, gather
import asyncio


async def my_func_async():
    print('my_func_async b4 await')
    result = await my_func_async_3()
    print('my_func_async after await')


async def my_func_async_2():
    print('do my code my_func_async')


async def my_func_async_3():
    print('my_func_async_3')
    return 5


def my_func_generator():
    print('do my code')
    count = 0
    while True:
        print('step')
        count += 1
        yield count
        print('after yield')


def my_func_coroutine():
    print('do my code')
    count = 0
    static = []
    static_data = yield
    while True:
        data = {}
        data['stan'][0]['people'] = 89
        static.append(data)
        static_data = yield static_data



if __name__ == '__main__':
    my_coroutine = my_func_coroutine()
    print(my_coroutine.send(None))
    data = {1: 1}
    static = my_coroutine.send(data)
    my_coroutine.send(data)
    print('==================')
    my_coroutine.send(333)

    # print(my_coroutine)


    # loop = get_event_loop()
    # task = loop.create_task(my_func_async())
    # wait_tasks = asyncio.wait([task])
    #
    # loop.run_until_complete(wait_tasks)
    # loop.run_forever()
