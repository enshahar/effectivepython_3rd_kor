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


print("Example 2")
baby_names = {
    "cat": "kitten",
    "dog": "puppy",
}
print(baby_names)


print("Example 4")
print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))
print(baby_names.popitem())  # Last item inserted


print("Example 6")
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

my_func(goose="gosling", kangaroo="joey")


print("Example 8")
class MyClass:
    def __init__(self):
        self.alligator = "hatchling"
        self.elephant = "calf"

a = MyClass()
for key, value in a.__dict__.items():
    print(f"{key} = {value}")


print("Example 9")
votes = {
    "otter": 1281,
    "polar bear": 587,
    "fox": 863,
}


print("Example 10")
def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


print("Example 11")
def get_winner(ranks):
    return next(iter(ranks))


print("Example 12")
ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)


print("Example 13")
from collections.abc import MutableMapping

class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)


my_dict = SortedDict()
my_dict["otter"] = 1
my_dict["cheeta"] = 2
my_dict["anteater"] = 3
my_dict["deer"] = 4

assert my_dict["otter"] == 1

assert "cheeta" in my_dict
del my_dict["cheeta"]
assert "cheeta" not in my_dict

expected = [("anteater", 3), ("deer", 4), ("otter", 1)]
assert list(my_dict.items()) == expected

assert not isinstance(my_dict, dict)


print("Example 14")
sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)


print("Example 15")
def get_winner(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name

winner = get_winner(sorted_ranks)
print(winner)


print("Example 16")
try:
    def get_winner(ranks):
        if not isinstance(ranks, dict):
            raise TypeError("must provide a dict instance")
        return next(iter(ranks))
    
    
    assert get_winner(ranks) == "otter"
    
    get_winner(sorted_ranks)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False
