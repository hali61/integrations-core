import time
import random
import ray


@ray.remote
def echo_sleep(x):
    print(f"{time.time()} - {x}")
    time.sleep(x)
    return x


while True:
    ray.init(address="ray://ray-head:10001")

    result_ids = []
    for i in range(random.randint(3, 10)):
        result_ids.append(echo_sleep.remote(i))

    # Wait for the tasks to complete and retrieve the results.
    print(f"{time.time()} - {ray.get(result_ids)}")

    ray.shutdown()

    print(f"{time.time()} - Sleeping for 30 seconds")
    time.sleep(30)
