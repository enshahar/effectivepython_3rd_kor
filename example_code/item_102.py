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
data = list(range(10**5))
index = data.index(91234)
assert index == 91234


print("Example 2")
def find_closest(sequence, goal):
    for index, value in enumerate(sequence):
        if goal < value:
            return index
    raise ValueError(f"{goal}이 범위를 벗어남")

index = find_closest(data, 91234.56)
assert index == 91235

try:
    find_closest(data, 100000000)
except ValueError:
    pass  # 예외가 발생해 이 줄이 실행됨
else:
    assert False


print("Example 3")
from bisect import bisect_left

index = bisect_left(data, 91234)     # 정확히 일치
assert index == 91234

index = bisect_left(data, 91234.56)  # 근접한 값과 일치
assert index == 91235


print("Example 4")
import random
import timeit

size = 10**5
iterations = 1000

data = list(range(size))
to_lookup = [random.randint(0, size) for _ in range(iterations)]

def run_linear(data, to_lookup):
    for index in to_lookup:
        data.index(index)

def run_bisect(data, to_lookup):
    for index in to_lookup:
        bisect_left(data, index)

baseline = (
    timeit.timeit(
        stmt="run_linear(data, to_lookup)",
        globals=globals(),
        number=10,
    )
    / 10
)
print(f"선형 탐색: {baseline:.6f}초")

comparison = (
    timeit.timeit(
        stmt="run_bisect(data, to_lookup)",
        globals=globals(),
        number=10,
    )
    / 10
)
print(f"이진 탐색: {comparison:.6f}초")

slowdown = 1 + ((baseline - comparison) / comparison)
print(f"{slowdown:.1f}배 느림")
