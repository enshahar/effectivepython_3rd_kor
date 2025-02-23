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
class ZooDatabase:

    def get_animals(self, species):
        pass

    def get_food_period(self, species):
        pass

    def feed_animal(self, name, when):
        pass


print("Example 2")
from datetime import datetime

def do_rounds(database, species, *, now_func=datetime.now):
    now = now_func()
    feeding_timedelta = database.get_food_period(species)
    animals = database.get_animals(species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) >= feeding_timedelta:
            database.feed_animal(name, now)
            fed += 1

    return fed


print("Example 3")
from unittest.mock import Mock

database = Mock(spec=ZooDatabase)
print(database.feed_animal)
database.feed_animal()
database.feed_animal.assert_any_call()


print("Example 4")
from datetime import timedelta
from unittest.mock import call

now_func = Mock(spec=datetime.now)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

database = Mock(spec=ZooDatabase)
database.get_food_period.return_value = timedelta(hours=3)
database.get_animals.return_value = [
    ("점박이", datetime(2019, 6, 5, 11, 15)),
    ("털복숭이", datetime(2019, 6, 5, 12, 30)),
    ("조조", datetime(2019, 6, 5, 12, 55)),
]


print("Example 5")
result = do_rounds(database, "미어캣", now_func=now_func)
assert result == 2

database.get_food_period.assert_called_once_with("미어캣")
database.get_animals.assert_called_once_with("미어캣")
database.feed_animal.assert_has_calls(
    [
        call("점박이", now_func.return_value),
        call("털복숭이", now_func.return_value),
    ],
    any_order=True,
)


print("Example 6")
try:
    database.bad_method_name()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 7")
DATABASE = None

def get_database():
    global DATABASE
    if DATABASE is None:
        DATABASE = ZooDatabase()
    return DATABASE

def main(argv):
    database = get_database()
    species = argv[1]
    count = do_rounds(database, species)
    print(f"{count} {species}에게 먹이를 줍니다")
    return 0


print("Example 8")
import contextlib
import io
from unittest.mock import patch

with patch("__main__.DATABASE", spec=ZooDatabase):
    now = datetime.now()

    DATABASE.get_food_period.return_value = timedelta(hours=3)
    DATABASE.get_animals.return_value = [
        ("점박이", now - timedelta(minutes=4.5)),
        ("털복숭이", now - timedelta(hours=3.25)),
        ("조조", now - timedelta(hours=3)),
    ]

    fake_stdout = io.StringIO()
    with contextlib.redirect_stdout(fake_stdout):
        main(["program name", "미어켓"])

    found = fake_stdout.getvalue()
    expected = "2 미어켓에게 먹이를 줍니다\n"

    assert found == expected
