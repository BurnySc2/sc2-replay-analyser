# distutils: language=c++
# cython: language_level=3

from cpython cimport array
import array

# Import https://en.cppreference.com/w/cpp/container/map
# See what is available: https://github.com/cython/cython/tree/master/Cython/Includes/libcpp python3.7/site-packages/Cython/Includes/libcpp
from libcpp.vector cimport vector as cpp_vector
from libcpp.map cimport map as cpp_map
from libcpp.unordered_map cimport unordered_map as cpp_unordered_map
from libcpp.set cimport set as cpp_set

from libcpp.deque cimport deque as cpp_deque
from libcpp.queue cimport queue as cpp_queue, priority_queue as cpp_priority_queue
from libcpp.stack cimport stack as cpp_stack

"""
TODO Write example for:
    int - uint, int64?
    float - double
    string - does it work?
    tuple - ?
    list - vector
    set - set
    dict - map
    numpy array - ?
manipulation
"""


def two_sum(list nums, int target):
    """
    Given an array of integers, return indices of the two numbers such that they add up to a specific target.

    You may assume that each input would have exactly one solution, and you may not use the same element twice.

    Example:
        Given nums = [2, 7, 11, 15], target = 9,

        Because nums[0] + nums[1] = 2 + 7 = 9,
        return [0, 1].
    """
    cdef:
        cpp_map[int, int] my_dict
        int val, value, index
    for index, value in enumerate(nums):
        val = target - value
        if my_dict.count(val) > 0:
            return [my_dict[val], index]
        my_dict[value] = index


def two_sum_vector(cpp_vector[int] nums, int target):
    cdef:
        cpp_map[int, int] my_dict
        int val, value, index
    for index, value in enumerate(nums):
        val = target - value
        if my_dict.count(val) > 0:
            return [my_dict[val], index]
        my_dict[value] = index


def primes(int nb_primes):
    """ Find the first X amount of primes"""
    cdef:
        int n, i, len_p
        int[10000] p
    if nb_primes > 10000:
        nb_primes = 10000
    len_p = 1  # The current number of elements in p
    p[0] = 2
    n = 3
    while len_p < nb_primes:
        # Is n prime?
        for i in p[:len_p]:
            if n % i == 0:
                break
        # If no break occurred in the loop, we have a prime
        else:
            p[len_p] = n
            len_p += 1
        n += 2
    # Let's return the result in a python list
    return [i for i in p[:len_p]]


def primes_vector(unsigned int nb_primes):
    cdef:
        int n, i
        cpp_vector[int] p
    # p.reserve(nb_primes)
    p.push_back(2)
    n = 3
    while p.size() < nb_primes:
        for i in p:
            if n % i == 0:
                break
        else:
            p.push_back(n)
        n += 2
    return p



ctypedef cpp_vector[int] point
# ctypedef cpp_map[point, point] my_map
# cdef int in_bounds(int y, int x, int height, int width):
#     if 0 <= y < height and 0 <= x < width:
#         return 1
#     return 0
#
# cdef int is_wall(long[:, :] grid, int y, int x):
#     if grid[y, x] == 0:
#         return 1
#     return 0
#

# cdef cppclass MyNode:
#     float distance
#     point current
#     point previous
#     # 'Less than' trait https://stackoverflow.com/questions/22537683/how-to-make-a-c-mapping-from-c-struct-to-int-in-cython
#     bint lessthan "operator<"(const MyNode t) const:
#          return this.distance > t.distance

def test_map(cpp_map[point, point] came_from, point p):
    came_from[[1, 2]] = [3, 4]
    return came_from[p]
def test_vec(list my_vec, (int, int) p):
    my_vec.append(p)
    return my_vec

from libcpp.algorithm cimport push_heap, pop_heap
def test_p_queue(queue, a, b, c):
    # cdef cpp_priority_queue[int] my_queue
    push_heap(queue, a)
    push_heap(queue, b)
    push_heap(queue, c)
    # my_queue.push(a)
    # my_queue.push(b)
    # my_queue.push(c)
    return queue

"""
cython question:


"""

# cdef cpp_vector[point] generate_path(my_map came_from, point start, point goal):
#     cdef cpp_vector[point] path
#     while start != goal:
#         path.push_back(goal)
#         goal = came_from[goal]
#     return path
#

# Constructor of 'MyNode'
# cdef MyNode make_node(float distance, point current, point previous) nogil:
#     cdef MyNode node
#     node.distance = distance
#     node.current = current
#     node.previous = previous
#     return node


# def dijkstra(long[:, :] grid, start, goal, diagonal=False):
#     return dijkstra_(grid, start, goal, diagonal)


from collections import deque
# from collections cimport deque
from heapq import heappush, heappop
# from heapq cimport heappush, heappop


# cdef (double, cpp_vector[(int, int)]) dijkstra_(long[:, :] grid, start, goal, diagonal=False):
#     cdef:
#         int neighbors_amount
#     if start == goal:
#         return 0, []
#     open_set = [(0, start, None)]
#     neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
#     sqrt2 = 2 ** 0.5
#     distances = [1., 1., 1., 1., sqrt2, sqrt2, sqrt2, sqrt2]
#     neighbors_amount = 4
#     if diagonal:
#         neighbors_amount = 8
#     height = grid.shape[0]
#     width = grid.shape[1]
#     distance_dict = {}
#     came_from = {}
#
#     def in_bounds(point) -> bool:
#         nonlocal height, width
#         return 0 <= point[0] < height and 0 <= point[1] < width
#
#     def is_wall(point) -> bool:
#         nonlocal grid
#         return grid[point[0]][point[1]] != 0
#
#     def generate_path():
#         path = []
#         current = goal
#         while current != start:
#             path.append(current)
#             current = came_from[current]
#         return path



    # while open_set:
    #     current_distance, current_point, previous_point = heappop(open_set)
    #     if current_point in came_from:
    #         continue
    #     distance_dict[current_point] = current_distance
    #     came_from[current_point] = previous_point
    #     for node_dist, neighbor in zip(distances, neighbors):
    #         new_point = current_point[0] + neighbor[0], current_point[1] + neighbor[1]
    #         if not in_bounds(new_point):
    #             continue
    #         if is_wall(new_point):
    #             continue
    #         new_distance = current_distance + node_dist
    #         if new_point in distance_dict and distance_dict[new_point] >= new_distance:
    #             continue
    #         heappush(open_set, (new_distance, new_point, current_point))
    #     if goal in came_from:
    #         return distance_dict[goal], generate_path()
    # return -1, []