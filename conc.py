import asyncio
import time
import random
import signal
import matplotlib.pyplot as plt

start = time.time()
queue = asyncio.Queue()

def print_info(s):
    print(f"{round(time.time() - start, 3)} {s}")

class Car:
    def __init__(self, n, size):
        self.n = n
        self.size = size

class PetrolStation:
    SPEED = 7

    def __init__(self, n):
        self.n = n

    async def refuel(self):
        while True:
            car = await queue.get()
            print_info(f"{car.n}: Refueling started ({self.n})")
            await asyncio.sleep(car.size / self.SPEED)
            print_info(f"{car.n}: Refueling ended ({self.n})")

async def main():
    n = 1
    while True:
        print_info(f"Queue size = {queue.qsize()}")
        car = Car(n, random.random() * 20 + 35)
        print_info(f"{n}: Car arrived")
        await queue.put(car)
        await asyncio.sleep(random.random())
        n += 1


def termination_handler(*args, **kwargs):
    plt.plot([1, 2, 3], [1, 2, 3])
    plt.show()
    exit()


signal.signal(signal.SIGINT, termination_handler)
loop = asyncio.get_event_loop()
for i in range(12):
    loop.create_task(PetrolStation(i + 1).refuel())
loop.create_task(main())
loop.run_forever()
