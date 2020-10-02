from contextlib import contextmanager
from typing import Generator, List, Any, Dict
from math import factorial

from loguru import logger
import time

"""
These are lexicographically ordered permutations.
"""


def permutation(my_list: List[Any]) -> List[Any]:
    assert len(my_list) > 0
    if len(my_list) == 1:
        return [my_list]
    result = []
    for i in range(len(my_list)):
        middle = my_list[i]
        remaining_list = my_list[:i] + my_list[i + 1 :]
        for p in permutation(remaining_list):
            result.append([middle] + p)
    return result


def permutation_generator(my_list: List[Any]) -> Generator[Any, None, None]:
    assert len(my_list) > 0
    if len(my_list) == 1:
        yield my_list
        return
    for i, middle in enumerate(my_list):
        remaining_list = my_list[:i] + my_list[i + 1 :]
        for p in permutation_generator(remaining_list):
            yield [middle] + p


def permutation_backwards_generator(my_list: List[Any]) -> Generator[Any, None, None]:
    assert len(my_list) > 0
    if len(my_list) == 1:
        yield my_list
        return
    for i in reversed(range(len(my_list))):
        middle = my_list[i]
        remaining_list = my_list[:i] + my_list[i + 1 :]
        for p in permutation_backwards_generator(remaining_list):
            yield [middle] + p


def get_index_of_permutation(original: List[Any], perm: List[Any]) -> int:
    """ Returns the index of a lexicographically ordered permutation.
    assert get_index_of_permutation(list("ABC"), list("ABC")) == 0
    assert get_index_of_permutation(list("ABC"), list("CBA")) == 5
    assert get_index_of_permutation(list("ABCD"), list("DCBA")) == 23
    """
    assert len(original) == len(perm)
    result, factor, cur, length = 0, 1, 1, len(perm)
    values = {char: i for i, char in enumerate(original)}
    for j in reversed(range(length)):
        result += factor * sum(1 for i in perm[j + 1 :] if values[i] < values[perm[j]])
        factor *= cur
        cur += 1
    return result


def get_permutation_at_index(original: List[Any], index: int) -> List[Any]:
    """ Returns lexicographically ordered permutation at index 'index'.
    assert get_permutation_at_index(list("ABC"), 0) == list("ABC")
    assert get_permutation_at_index(list("ABC"), 5) == list("CBA")
    assert get_permutation_at_index(list("ABCD"), 23) == list("DCBA")
    """
    assert 0 <= index < factorial(len(original))
    if len(original) == 1:
        return original
    quotient, remainder = divmod(index, factorial(len(original) - 1))
    return [original[quotient]] + get_permutation_at_index(original[:quotient] + original[quotient + 1 :], remainder)


def get_next_permutation(perm: List[Any]):
    if len(perm) <= 1:
        return perm
    for i in reversed(range(len(perm) - 1)):
        last = perm[i]
        for j in reversed(range(i + 1, len(perm))):
            prev = perm[j]
            if prev > last:
                perm[i], perm[j] = perm[j], perm[i]
                if len(perm[i + 1 :]) > 1:
                    perm[i + 1 :] = sorted(perm[i + 1 :])
                return perm
    perm.sort()
    return perm


def get_previous_permutation(perm: List[Any]):
    if len(perm) <= 1:
        return perm
    for i in reversed(range(len(perm) - 1)):
        last = perm[i]
        for j in reversed(range(i + 1, len(perm))):
            prev = perm[j]
            if prev < last:
                perm[i], perm[j] = perm[j], perm[i]
                if len(perm[i + 1 :]) > 1:
                    perm[i + 1 :] = sorted(perm[i + 1 :], reverse=True)
                return perm
    perm.sort(reverse=True)
    return perm


def _test_permutations(limit: int = 6):
    correct_perms = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    for p, correct in zip(permutation_generator(list("ABC")), correct_perms):
        assert p == list(correct)

    assert get_index_of_permutation(list("ABC"), list("ABC")) == 0
    assert get_index_of_permutation(list("ABC"), list("ACB")) == 1
    assert get_index_of_permutation(list("ABC"), list("BAC")) == 2
    assert get_index_of_permutation(list("ABC"), list("BCA")) == 3
    assert get_index_of_permutation(list("ABC"), list("CAB")) == 4
    assert get_index_of_permutation(list("ABC"), list("CBA")) == 5

    assert get_index_of_permutation(list("ABCD"), list("ABCD")) == 0
    assert get_index_of_permutation(list("ABCD"), list("DCBA")) == 23

    assert list(permutation_generator(list("ABCD"))) == list(
        reversed(list(permutation_backwards_generator(list("ABCD"))))
    )

    assert get_next_permutation(list("ABC")) == list("ACB"), get_next_permutation(list("ABC"))
    assert get_next_permutation(list("ACB")) == list("BAC"), get_next_permutation(list("ACB"))
    assert get_next_permutation(list("CBA")) == list("ABC"), get_next_permutation(list("CBA"))

    assert get_previous_permutation(list("ACB")) == list("ABC"), get_previous_permutation(list("ABC"))
    assert get_previous_permutation(list("BAC")) == list("ACB"), get_previous_permutation(list("ACB"))
    assert get_previous_permutation(list("ABC")) == list("CBA"), get_previous_permutation(list("CBA"))

    prev = None
    for p in permutation_generator(list("ABCD")):
        if prev is not None:
            assert prev == get_previous_permutation(p.copy()), (prev, get_previous_permutation(p.copy()))
            assert p == get_next_permutation(prev.copy()), (p, get_next_permutation(prev.copy()))
        prev = p

    from string import ascii_uppercase

    for length in range(1, limit):
        string = ascii_uppercase[:length]
        for index, perm in enumerate(permutation_generator(list(string))):
            perm2 = get_permutation_at_index(list(string), index)
            index2 = get_index_of_permutation(list(string), perm)
            assert index == index2
            assert perm == perm2


if __name__ == "__main__":
    _test_permutations()

    @contextmanager
    def time_this(label: str):
        start = time.perf_counter_ns()
        try:
            yield
        finally:
            end = time.perf_counter_ns()
            logger.info(f"TIME {label}: {(end-start)/1e9} sec")

    with time_this("Permutation"):
        for n in range(10 ** 4):
            data = list("123")
            for p in permutation_generator(data):
                pass
            for p in permutation_backwards_generator(data):
                pass

    # data = list("123")
    # for p in permutation_generator(data):
    #     print(p)
    #
    # print("###################")
    #
    # for p in permutation_backwards_generator(data):
    #     print(p)

    data = list("1234567")
    assert list(permutation_generator(data)) == list(permutation_backwards_generator(data))[::-1]
