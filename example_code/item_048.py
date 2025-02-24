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
names = ["소크라테스", "아르키메데스", "플라톤", "아리스토텔레스"]
names.sort(key=len)
print(names)


print("Example 2")
def log_missing():
    print("키가 추가됨")
    return 0


print("Example 3")
from collections import defaultdict

current = {"초록": 12, "파랑": 3}
increments = [
    ("빨강", 5),
    ("파랑", 17),
    ("주황", 9),
]
result = defaultdict(log_missing, current)
print("이전:", dict(result))
for key, amount in increments:
    result[key] += amount
print("이후:", dict(result))


print("Example 4")
def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # 상태가 있는 클로저
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


print("Example 5")
result, count = increment_with_report(current, increments)
assert count == 2
print(result)


print("Example 6")
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


print("Example 7")
counter = CountMissing()
result = defaultdict(counter.missing, current)  # 메서드 참조
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print(result)


print("Example 8")
class BetterCountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)


print("Example 9")
counter = BetterCountMissing()
result = defaultdict(counter, current)  # __call__에 의존함
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print(result)
