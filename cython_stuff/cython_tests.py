# Compile using:
# cythonize -a -i cython_examples.pyx
from contextlib import contextmanager
import time

from loguru import logger
import numpy as np

from cython_stuff.cython_examples import two_sum, two_sum_vector, primes, primes_vector, test_map, test_vec
from cython_stuff.python_examples import two_sum_slow, primes_slow, dijkstra_slow


@contextmanager
def time_this(label: str):
    start = time.perf_counter_ns()
    try:
        yield
    finally:
        end = time.perf_counter_ns()
        logger.info(f"TIME {label}: {(end-start)/1e9} sec")


# Use like this
if __name__ == "__main__":
    # d = {(1, 2): (3, 4)}
    # print(test_map({}, [1, 2]))
    print(test_vec([], (1, 2)))

    # limit = 10 ** 3
    # grid = np.array(
    #     [
    #         [1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 1, 1, 1, 1, 0, 1, 1],
    #         [1, 1, 1, 1, 1, 0, 1, 1],
    #         [1, 1, 1, 1, 1, 0, 1, 1],
    #         [1, 1, 0, 0, 0, 0, 1, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1],
    #     ]
    # )
    # start = (0, 0)
    # end = (7, 7)
    # path = dijkstra(grid, start, end, True)
    # logger.info(f"Path: {path}")
    #
    # with time_this("Dijkstra cython"):
    #     for n in range(limit):
    #         dijkstra(grid, start, end)
    # with time_this("Dijkstra cython diagonal"):
    #     for n in range(limit):
    #         dijkstra(grid, start, end, True)
    #
    # with time_this("Dijkstra native"):
    #     for n in range(limit):
    #         dijkstra_slow(grid, start, end)
    # with time_this("Dijkstra native diagonal"):
    #     for n in range(limit):
    #         dijkstra_slow(grid, start, end, True)

    # Test two sum, which uses array or cpp vector (and both use cpp map)
    # limit = 10 ** 4
    # my_list = list(range(5, 10**3)) + [4]
    # my_target = 9
    # result1 = two_sum(my_list, my_target)
    # result2 = two_sum_slow(my_list, my_target)
    # assert result1 == result2, f"{result1}\n{result2}"
    # logger.info(f"Result two sum: {result1}")
    # with time_this("Two sum Cython Array"):
    #     for n in range(limit):
    #         two_sum(my_list, my_target)
    # with time_this("Two sum Cython Vector"):
    #     for n in range(limit):
    #         two_sum_vector(my_list, my_target)
    # with time_this("Two sum Native"):
    #     for n in range(limit):
    #         two_sum_slow(my_list, my_target)
    #
    # # Test primes
    # limit = 10 ** 1
    # amount = 1999
    # with time_this("Primes Cython Array"):
    #     for n in range(limit):
    #         primes(amount)
    # with time_this("Primes Cython Vector"):
    #     for n in range(limit):
    #         primes_vector(amount)
    # with time_this("Primes Native"):
    #     for n in range(limit):
    #         primes_slow(amount)
    #
    # assert primes_vector(amount) == primes_slow(amount), f"{primes_vector(amount)}\n{primes_slow(amount)}"
    # assert primes(amount) == primes_slow(amount), f"{primes(amount)}\n{primes_slow(amount)}"

time.sleep(0.1)
