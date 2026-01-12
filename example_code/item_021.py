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

print("아이템 21")
print("Example 1")
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


print("Example 2")
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


print("Example 3")
path = "my_numbers.txt"
with open(path, "w") as f:
    for i in (15, 35, 80):
        f.write(f"{i}\n")

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


print("Example 4")
it = read_visits("my_numbers.txt")
percentages = normalize(it)
print(percentages)


print("Example 5")
it = read_visits("my_numbers.txt")
print(list(it))
print(list(it))  # 이미 모든 원소를 다 소진했다


print("Example 6")
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # 이터레이터 복사
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


print("Example 7")
it = read_visits("my_numbers.txt")
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


print("Example 8")
def normalize_func(get_iter):
    total = sum(get_iter())   # 새 이터레이터
    result = []
    for value in get_iter():  # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result


print("Example 9")
path = "my_numbers.txt"
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0


print("Example 10")
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


print("Example 11")
visits = ReadVisits(path)
percentages = normalize(visits)  # 변경함
print(percentages)
assert sum(percentages) == 100.0


print("Example 12")
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # 이터레이터 -- 나쁨!
        raise TypeError("컨테이너를 제공해야 함")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
normalize_defensive(visits)  # 오류 없음

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


print("Example 13")
from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # 반복 가능한 이터레이터인지 검사하는 다른 방법
        raise TypeError("Must supply a container")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
normalize_defensive(visits)  # 오류 없음

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


print("Example 14")
visits_list = [15, 35, 80]
list_percentages = normalize_defensive(visits_list)

visits_obj = ReadVisits(path)
obj_percentages = normalize_defensive(visits_obj)

assert list_percentages == obj_percentages
assert sum(percentages) == 100.0


print("Example 15")
try:
    visits = [15, 35, 80]
    it = iter(visits)
    normalize_defensive(it)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False
