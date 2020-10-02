from typing import List
from heapq import heappush, heappop, heappushpop


def two_sum_slow(nums: List[int], target: int) -> List[int]:
    my_dict = {}
    for index, value in enumerate(nums):
        val = target - value
        if val in my_dict:
            return [my_dict[val], index]
        my_dict[value] = index


def primes_slow(nb_primes: int):
    """ Find the first X amount of primes. """
    primes = []
    len_p = 0  # The current number of elements in primes.
    n = 2
    while len_p < nb_primes:
        # Is n prime?
        for i in primes[:len_p]:
            if n % i == 0:
                break
        # If no break occurred in the loop, we have a prime.
        else:
            primes.append(n)
            len_p += 1
        n += 1

    # Let's return the result in a python list:
    return primes


from typing import Tuple, Dict, Deque, Optional
import numpy as np

from collections import deque


def dijkstra_slow(
    grid: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int], diagonal=False
) -> Tuple[float, Deque[Tuple[int, int]]]:
    if start == goal:
        return 0, deque()
    open_set: List[Tuple[int, Tuple[int, int], Optional[Tuple[int, int]]]] = [(0, start, None)]
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    sqrt2 = 2 ** 0.5
    distances: List[float] = [1.0] * 4 + [sqrt2] * 4
    if diagonal:
        neighbors += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    height, width = grid.shape
    distance_dict: Dict[Tuple[int, int], float] = {}
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

    def in_bounds(point: Tuple[int, int]) -> bool:
        nonlocal height, width
        return 0 <= point[0] < height and 0 <= point[1] < width

    def is_wall(point: Tuple[int, int]) -> bool:
        nonlocal grid
        return not grid[point]

    def generate_path() -> Deque[Tuple[int, int]]:
        path: Deque[Tuple[int, int]] = deque()
        current = goal
        while current != start:
            path.appendleft(current)
            current = came_from[current]
        return path

    while open_set:
        current_distance, current_point, previous_point = heappop(open_set)
        if current_point in came_from:
            continue
        distance_dict[current_point] = current_distance
        came_from[current_point] = previous_point
        for node_dist, neighbor in zip(distances, neighbors):
            new_point = current_point[0] + neighbor[0], current_point[1] + neighbor[1]
            if not in_bounds(new_point):
                continue
            if is_wall(new_point):
                continue
            new_distance = current_distance + node_dist
            if new_point in distance_dict and distance_dict[new_point] >= new_distance:
                continue
            heappush(open_set, (new_distance, new_point, current_point))
        if goal in came_from:
            return distance_dict[goal], generate_path()
    return -1, deque()
