# Other
import time
import os
import sys
import re
import time
import json
from contextlib import contextmanager
from pathlib import Path
from dataclasses import dataclass

# https://pypi.org/project/dataclasses-json/#description
from dataclasses_json import DataClassJsonMixin

# Coroutines and multiprocessing
import asyncio
import aiohttp
from multiprocessing import Process, Lock, Pool

# Simple logging https://github.com/Delgan/loguru
from loguru import logger

# Database
import sqlite3

# Remove previous default handlers2
logger.remove()
# Log to console
logger.add(sys.stdout, level="INFO")
# Log to file, max size 1 mb
logger.add("main.log", rotation="1 MB", retention="7 days", level="INFO")

# Type annotation / hints
from typing import List, Iterable, Union, Set


async def main():
    logger.info("Simple {} logger output", "loguru")

    regex_match_test()

    measure_time()

    sites: List[str] = ["http://www.jython.org", "http://olympus.realpython.org/dice"] * 80
    start_time = time.perf_counter()
    await download_all_sites(sites)

    # Download an image with download speed throttle
    async with aiohttp.ClientSession() as session:
        result: bool = await download_image(
            session,
            url="https://file-examples.com/wp-content/uploads/2017/10/file_example_PNG_1MB.png",
            file_path=Path("test/image.png"),
            temp_file_path=Path("test/image_download_not_complete"),
            # Download at speed of 100kb/s
            download_speed=100 * 2 ** 10,
        )

    end_time = time.perf_counter()
    logger.info(f"Time for sites download taken: {end_time - start_time}")

    math_result = await do_math(6)

    start_time = time.perf_counter()
    do_multiprocessing()
    end_time = time.perf_counter()
    logger.info(f"Time for multiprocessing taken: {end_time - start_time}")

    mass_replace()

    logger.info(f"Creating hello world file...")
    create_file()

    logger.info(f"Testing writing dataclass to json and re-load and compare both objects")
    test_data_class_to_and_from_json()

    logger.info(f"Validating all roman numbers up to 3999")
    test_all_roman_numbers()

    logger.info(f"Testing database interaction")
    test_database()
    test_database_with_classes()


def measure_time():
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
        with time_this("square rooting"):
            for n in range(10 ** 4):
                x = n ** 0.5


def regex_match_test():
    """
    Match pattern:
    HH:MM:SS
    """
    assert re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})", "00:00:00")
    assert not re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})", "0:00:00")
    assert not re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})", "00:0:00")
    assert not re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})", "00:00:0")
    assert not re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})", "00:0000")

    pattern = "^(1110)|(0111)$|(01110)|^(111)$"
    p = re.compile(pattern)

    assert p.search("111") and p.match("111")
    assert p.search("0111") and p.match("0111")
    # Why does it not match here?
    assert p.search("00111") and not p.match("00111")
    assert p.search("1110") and p.match("1110")
    assert p.search("01110") and p.match("01110")
    assert not p.search("011110") and not p.match("011110")
    assert not p.search("01111") and not p.match("01111")
    assert not p.search("11110") and not p.match("11110")

    pattern = "^(10)|(01)$|(010)|^(1)$"
    p = re.compile(pattern)
    # Why does it not match here?
    assert p.search("11101") and not p.match("11101")


def generate_roman_number(n: int) -> str:
    """
    Allowed roman numbers:
    IV, VI, IX, XI, XC, LC, XXXIX, XLI
    Disallowed:
    IIV, VIIII, XXXX, IXL, XIL
    """
    if 4000 < n:
        raise ValueError(f"Input too big: {n}")
    number_list = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    string_as_list = []
    for divisor, character in number_list:
        if n >= divisor:
            count, n = divmod(n, divisor)
            string_as_list.extend(count * [character])
    return "".join(string_as_list)


def regex_match_roman_number(roman_number: str) -> bool:
    """ Returns True if input string is a roman number
    First row: Look ahead -> dont match empty string
    Second row: 1000-3000
    Third row: 3400 or 3900, connected with 100, 200, 300, or 500, 600, 700 or 800
    Same pattern for 4th and 5th row
    """
    numbers_1_to_3999 = """
    (?=[MDCLXVI])
        M{0,3}
            ( C[MD] | D?C{0,3} )
                ( X[CL] | L?X{0,3} )
                    ( I[XV] | V?I{0,3} )
    """.replace(
        " ", ""
    ).replace(
        "\n", ""
    )
    return bool(re.fullmatch(numbers_1_to_3999, roman_number))


def test_all_roman_numbers():
    for i in range(1, 4000):
        assert regex_match_roman_number(generate_roman_number(i)), f"{generate_roman_number(i)} != {i}"
        if i == 3999:
            logger.info(f"3999 in roman number is: {generate_roman_number(i)}")


async def download_image(
    session: aiohttp.ClientSession,
    url: str,
    file_path: Path,
    temp_file_path: Path,
    download_speed: int = -1,
    chunk_size: int = 1024,
) -> bool:
    """
    Downloads an image (or a file even) from "url" and saves it to "temp_file_path". When the download is complete, it renames the file at "temp_file_path" to "file_path".
    It respects "download_speed" in bytes per second. If no parameter was given, it will ignore the download limit.

    Returns boolean if download was successful.
    """
    downloaded: int = 0
    # Download start time
    time_last_subtracted = time.perf_counter()
    # Affects sleep time and check size for download speed, should be between 0.1 and 1
    accuracy: float = 0.1

    # Check if file exists
    if not file_path.exists():
        try:
            async with session.get(url) as response:
                # Assume everything went well with the response, no connection or server errors
                assert response.status == 200
                # Open file in binary write mode
                # with open(temp_file_path, "wb") as f:
                with temp_file_path.open("wb") as f:
                    # Download file in chunks
                    async for data in response.content.iter_chunked(chunk_size):
                        # Write data to file in asyncio-mode using aiofiles
                        f.write(data)
                        # Keep track of how much was downloaded
                        downloaded += chunk_size
                        # Wait if downloaded size has reached its download throttle limit
                        while 0 < download_speed and download_speed * accuracy < downloaded:
                            time_temp = time.perf_counter()
                            # This size should be the estimated downloaded size in the passed time
                            estimated_download_size = download_speed * (time_temp - time_last_subtracted)
                            downloaded -= estimated_download_size
                            time_last_subtracted = time_temp
                            await asyncio.sleep(accuracy)
            await asyncio.sleep(0.1)
            try:
                # os.rename(temp_file_path, file_path)
                temp_file_path.rename(file_path)
                return True
            except PermissionError:
                # The file might be open by another process
                logger.info(f"Permissionerror: Unable to rename file from ({temp_file_path}) to ({file_path})")
        except asyncio.TimeoutError:
            # The The server might suddenly not respond
            logger.info(f"Received timeout error in url ({url}) in file path ({file_path})!")
    else:
        # The file already exists!
        logger.info(f"File for url ({url}) in file path ({file_path}) already exists!")
    return False


async def download_site(session: aiohttp.ClientSession, url: str) -> aiohttp.ClientResponse:
    async with session.get(url) as response:
        return response


async def download_all_sites(sites: Iterable[str]) -> List[aiohttp.ClientResponse]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            # In python 3.7: asyncio.create_task instead of asyncio.ensure_future
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)

        # Run all tasks in "parallel" and wait until all of them are completed
        # responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Or to iterate over tasks as they complete (random order)
        responses = []
        for future in asyncio.as_completed(tasks):
            response = await future
            response_url = str(response.url)
            responses.append(response)

    return responses


async def do_math(number: Union[int, float]) -> Union[int, float]:
    return number + 3


def cpu_bound_summing(number: int) -> int:
    return sum(i * i for i in range(number))


def find_sums(numbers: Iterable[int]) -> List[int]:
    with Pool() as pool:
        result = pool.map(cpu_bound_summing, numbers)
    return result


def do_multiprocessing():
    numbers: List[int] = [5_000 + x for x in range(20)]
    sums: List[int] = find_sums(numbers)


def mass_replace():
    # Source: https://stackoverflow.com/a/6117124
    text = "my text cond\nition1 condition2"
    replace_dict = {"cond\nition1": "loves", "condition2": "fun"}
    # In case there is escape characters in k, it will not work without "re.escape"
    replace_dict = dict((re.escape(k), v) for k, v in replace_dict.items())
    pattern = re.compile("|".join(replace_dict.keys()))
    new_text = pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], text)
    logger.info(f"Mass replaced\n{text}\nto\n{new_text}")


def create_file():
    example_file_path = Path(__file__).parent / "hello_world.txt"
    with open(example_file_path, "w") as f:
        f.write("Hello world!\n")
    logger.info(f"Hello world file created in path {example_file_path}")


@dataclass()
class MyDataClass(DataClassJsonMixin):
    name: str
    value: int
    other: Set[int]


@dataclass()
class MyDataClassList(DataClassJsonMixin):
    some_dataclasses: List[MyDataClass]
    other_dataclasses: List[MyDataClass]


def save_objects_to_json(path: Path, my_dataclass_list: MyDataClassList):
    """ Save the given data class object to json file. """
    # Or: with open(path, "w") as f:
    with path.open("w") as f:
        f.write(my_dataclass_list.to_json(indent=4))


def load_objects_from_json(path: Path) -> MyDataClassList:
    """ Load a json file and re-create a data class list object from it. """
    # Or: with open(path) as f:
    with path.open() as f:
        return MyDataClassList.from_json(f.read())


def test_data_class_to_and_from_json():
    """ Creates a dataclass, saves to json, re-loads it from json file and compares them. """
    # Create objects
    # Note: interestingly the class holds a set but the written json file contains a list - reloading the list automatically converts it to a set again
    my_first_object = MyDataClass("burny", 420, {1, 2, 3})
    my_second_object = MyDataClass("not_burny", 123, {4, 2, 0})
    data_class_list = MyDataClassList([my_first_object], [my_second_object])

    # Write and reload from file
    test_path = Path("dataclass_test.json")
    save_objects_to_json(test_path, data_class_list)
    data_class_list_loaded = load_objects_from_json(test_path)

    # Compare
    assert data_class_list_loaded == data_class_list
    assert data_class_list_loaded.some_dataclasses[0] == data_class_list.some_dataclasses[0]
    assert data_class_list_loaded.other_dataclasses[0] == data_class_list.other_dataclasses[0]


def test_database():
    db = sqlite3.connect(":memory:")
    # db = sqlite3.connect("example.db")

    # Creates a new table "people" with 3 columns: text, real, integer
    # Fields marked with PRIMARY KEY are columns with unique values (?)
    db.execute("CREATE TABLE people (name text PRIMARY KEY, age integer, height real)")

    # Insert via string
    db.execute("INSERT INTO people VALUES ('Someone', 80, 1.60)")
    # Insert by tuple
    db.execute("INSERT INTO people VALUES (?, ?, ?)", ("Someone Else", 50, 1.65))

    friends = [
        ("Someone Else1", 40, 1.70),
        ("Someone Else2", 30, 1.75),
        ("Someone Else3", 20, 1.80),
        ("Someone Else4", 20, 1.85),
    ]
    # Insert many over iterable
    db.executemany("INSERT INTO people VALUES (?, ?, ?)", friends)

    # Delete an entry https://www.w3schools.com/sql/sql_delete.asp
    db.execute("DELETE FROM people WHERE age==40")

    # Update entries https://www.w3schools.com/sql/sql_update.asp
    db.execute("UPDATE people SET height=1.90, age=35 WHERE name=='Someone Else'")

    # Insert a value if it doesnt exist, or replace if it exists
    db.execute("REPLACE INTO people VALUES ('Someone Else5', 32, 2.01)")

    # Insert entries or update if it exists, 'upsert' https://www.sqlite.org/lang_UPSERT.html
    # Might not work on old sqlite3 versions
    # db.execute(
    #     "INSERT INTO people VALUES ('Someone Else', 35, 1.95) ON CONFLICT(name) DO UPDATE SET height=1.95, age=35"
    # )
    # db.execute(
    #     "INSERT INTO people VALUES ('Someone Else5', 32, 2.00) ON CONFLICT(name) DO UPDATE SET height=1.95, age=35"
    # )

    # Save database to hard drive, don't have to save when it is just in memory
    # db.commit()

    # SELECT: returns selected fields of the results, use * for all https://www.w3schools.com/sql/sql_select.asp
    # ORDER BY: Order by column 'age' and 'height' https://www.w3schools.com/sql/sql_orderby.asp
    # WHERE: Filters 'height >= 1.70' https://www.w3schools.com/sql/sql_where.asp
    for row in db.execute(
        "SELECT name, age, age, height FROM people WHERE height>=1.70 and name!='Someone Else2' ORDER BY age ASC, height ASC"
    ):
        logger.info(f"Row: {row}")

    # TODO: How to add or remove a column from existing database?

    db.close()


@dataclass
class Point:
    x: float
    y: float

    @staticmethod
    def serialize(p: "Point") -> bytes:
        return f"{p.x};{p.y}".encode("ascii")

    @staticmethod
    def deserialize(byte: bytes) -> "Point":
        x, y = list(map(float, byte.split(b";")))
        return Point(x, y)


def test_database_with_classes():
    # Register the adapter / serializer
    sqlite3.register_adapter(Point, Point.serialize)

    # Register the converter
    sqlite3.register_converter("point", Point.deserialize)

    db = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    # Creates new table
    db.execute("CREATE TABLE points (name text, p point)")

    points = [
        ["p1", Point(4.0, -3.2)],
        ["p2", Point(8.0, -6.4)],
    ]
    db.executemany("INSERT INTO points VALUES (?, ?)", points)
    for row in db.execute("SELECT * FROM points"):
        logger.info(f"Row: {row}")

    db.close()


if __name__ == "__main__":
    asyncio.run(main())
