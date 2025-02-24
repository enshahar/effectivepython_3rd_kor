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
import timeit

delay = timeit.timeit(stmt="1+2")
print(delay)


print("Example 2")
delay = timeit.timeit(stmt="1+2", number=100)
print(delay)


print("Example 3")
count = 1_000_000

delay = timeit.timeit(stmt="1+2", number=count)

print(f"{delay/count*1e9:.2f} 나노초")


print("Example 4")
import random

count = 100_000

delay = timeit.timeit(
    setup="""
numbers = list(range(10_000))
random.shuffle(numbers)
probe = 7_777
""",
    stmt="""
probe in numbers
""",
    globals=globals(),
    number=count,
)

print(f"{delay/count*1e9:.2f} 나노초")


print("Example 5")
delay = timeit.timeit(
    setup="""
numbers = set(range(10_000))
probe = 7_777
""",
    stmt="""
probe in numbers
""",
    globals=globals(),
    number=count,
)

print(f"{delay/count*1e9:.2f} 나노초")


print("Example 6")
def loop_sum(items):
    total = 0
    for i in items:
        total += i
    return total

count = 1000

delay = timeit.timeit(
    setup="numbers = list(range(10_000))",
    stmt="loop_sum(numbers)",
    globals=globals(),
    number=count,
)

print(f"{delay/count*1e9:.2f} 나노초")


print("Example 7")
print(f"{delay/count/10_000*1e9:.2f} 나노초")
