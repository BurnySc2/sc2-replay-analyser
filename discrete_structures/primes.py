from typing import List
import math
from collections import Counter


def sieve_of_eratosthenes(limit: int) -> List[int]:
    if limit < 2:
        return [False, False][:limit]
    sieve = [True for _ in range(0, limit)]
    sieve[:2] = [False, False]
    sieve[4::2] = [False] * len(sieve[4::2])

    value = 3
    primes = [2]
    while value < limit:
        if sieve[value]:
            primes.append(value)
            sieve[value ** 2 :: value] = [False] * len(sieve[value ** 2 :: value])
        value += 2
    return primes


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # For python 3.8: math.isqrt()
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def next_prime(n: int):
    if n < 2:
        return 2
    if n == 2:
        return 3
    n += 1 if n % 2 == 0 else 2
    while 1:
        if is_prime(n):
            return n
        n += 2


def prime_factors(n: int) -> Counter:
    prime = 2
    factors = Counter()
    while n > 1:
        assert prime <= n
        if n % prime == 0:
            factors[prime] += 1
            n //= prime
        else:
            prime = next_prime(prime)
    return factors


def test_prime_functions():
    for i in range(0, 100):
        sieve_of_eratosthenes(i)
    for i in sieve_of_eratosthenes(100):
        assert is_prime(i), (i, is_prime(i))

    not_primes = set(range(100)) - set(sieve_of_eratosthenes(100))
    for i in not_primes:
        assert not is_prime(i), (i, is_prime(i))

    for i in range(100):
        prime_factors(i)


if __name__ == "__main__":
    test_prime_functions()
