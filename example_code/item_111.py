#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2024 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### 책 예제에 맞는 환경 설정을 시작함
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# 모든 출력을 임시 디렉터리로 보냄
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# 윈도우에서 프로세스가 제대로 종료되도록 함
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)
### 책 예제에 맞는 환경설정 끝


print("Example 1")
class DatabaseConnection:
    def __init__(self, host, port):
        pass


class DatabaseConnectionError(Exception):
    pass

def get_animals(database, species):
    # Query the Database
    raise DatabaseConnectionError("Not connected")
    # Return a list of (name, last_mealtime) tuples


print("Example 2")
try:
    database = DatabaseConnection("localhost", "4444")
    
    get_animals(database, "Meerkat")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 3")
from datetime import datetime
from unittest.mock import Mock

mock = Mock(spec=get_animals)
expected = [
    ("Spot", datetime(2024, 6, 5, 11, 15)),
    ("Fluffy", datetime(2024, 6, 5, 12, 30)),
    ("Jojo", datetime(2024, 6, 5, 12, 45)),
]
mock.return_value = expected


print("Example 4")
try:
    mock.does_not_exist
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
database = object()
result = mock(database, "Meerkat")
assert result == expected


print("Example 6")
mock.assert_called_once_with(database, "Meerkat")


print("Example 7")
try:
    mock.assert_called_once_with(database, "Giraffe")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
from unittest.mock import ANY

mock = Mock(spec=get_animals)
mock("database 1", "Rabbit")
mock("database 2", "Bison")
mock("database 3", "Meerkat")

mock.assert_called_with(ANY, "Meerkat")


print("Example 9")
try:
    class MyError(Exception):
        pass
    
    mock = Mock(spec=get_animals)
    mock.side_effect = MyError("Whoops! Big problem")
    result = mock(database, "Meerkat")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 10")
def get_food_period(database, species):
    # Query the Database
    pass
    # Return a time delta

def feed_animal(database, name, when):
    # Write to the Database
    pass

def do_rounds(database, species):
    now = datetime.now()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


print("Example 11")
def do_rounds(
    database,
    species,
    *,
    now_func=datetime.now,
    food_func=get_food_period,
    animals_func=get_animals,
    feed_func=feed_animal
):
    now = now_func()
    feeding_timedelta = food_func(database, species)
    animals = animals_func(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed


print("Example 12")
from datetime import timedelta

now_func = Mock(spec=datetime.now)
now_func.return_value = datetime(2024, 6, 5, 15, 45)

food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)

animals_func = Mock(spec=get_animals)
animals_func.return_value = [
    ("Spot", datetime(2024, 6, 5, 11, 15)),
    ("Fluffy", datetime(2024, 6, 5, 12, 30)),
    ("Jojo", datetime(2024, 6, 5, 12, 45)),
]

feed_func = Mock(spec=feed_animal)


print("Example 13")
result = do_rounds(
    database,
    "Meerkat",
    now_func=now_func,
    food_func=food_func,
    animals_func=animals_func,
    feed_func=feed_func,
)

assert result == 2


print("Example 14")
from unittest.mock import call

food_func.assert_called_once_with(database, "Meerkat")

animals_func.assert_called_once_with(database, "Meerkat")

feed_func.assert_has_calls(
    [
        call(database, "Spot", now_func.return_value),
        call(database, "Fluffy", now_func.return_value),
    ],
    any_order=True,
)

# Make sure these variables don't pollute later tests
del food_func
del animals_func
del feed_func


print("Example 15")
from unittest.mock import patch

print("Outside patch:", get_animals)

with patch("__main__.get_animals"):
    print("Inside patch: ", get_animals)

print("Outside again:", get_animals)


print("Example 16")
try:
    fake_now = datetime(2024, 6, 5, 15, 45)
    
    with patch("datetime.datetime.now"):
        datetime.now.return_value = fake_now
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 17")
def get_do_rounds_time():
    return datetime.now()

def do_rounds(database, species):
    now = get_do_rounds_time()

with patch("__main__.get_do_rounds_time"):
    pass


print("Example 18")
def do_rounds(database, species, *, now_func=datetime.now):
    now = now_func()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


print("Example 19")
from unittest.mock import DEFAULT

with patch.multiple(
    "__main__",
    autospec=True,
    get_food_period=DEFAULT,
    get_animals=DEFAULT,
    feed_animal=DEFAULT,
):
    now_func = Mock(spec=datetime.now)
    now_func.return_value = datetime(2024, 6, 5, 15, 45)
    get_food_period.return_value = timedelta(hours=3)
    get_animals.return_value = [
        ("Spot", datetime(2024, 6, 5, 11, 15)),
        ("Fluffy", datetime(2024, 6, 5, 12, 30)),
        ("Jojo", datetime(2024, 6, 5, 12, 45)),
    ]


    print("Example 20")
    result = do_rounds(database, "Meerkat", now_func=now_func)
    assert result == 2

    get_food_period.assert_called_once_with(database, "Meerkat")
    get_animals.assert_called_once_with(database, "Meerkat")
    feed_animal.assert_has_calls(
        [
            call(database, "Spot", now_func.return_value),
            call(database, "Fluffy", now_func.return_value),
        ],
        any_order=True,
    )
