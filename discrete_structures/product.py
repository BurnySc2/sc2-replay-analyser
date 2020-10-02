from typing import Generator, List, Any, Iterable


def product_generator(*args: Iterable[Any], repeat: int = 1) -> Generator[Any, None, None]:
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield prod


if __name__ == "__main__":
    data1 = list("123")
    data2 = list("abc")

    for p in product_generator(data1, data2, repeat=2):
        print(p)
