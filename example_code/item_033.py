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

print("아이템 33")
print("Example 1")
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)

    values.sort(key=helper)


print("Example 2")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)


print("Example 3")
def sort_priority2(numbers, group):
    found = False         # 플래그의 초깃값

    def helper(x):
        if x in group:
            found = True  # 플래그를 설정함
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found          # 플래그의 최종 값


print("Example 4")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority2(numbers, group)
print("찾음:", found)
print(numbers)


print("Example 5")
try:
    foo = does_not_exist * 5
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 6")
def sort_priority2(numbers, group):
    found = False          # 영역: 'sort_priority2'

    def helper(x):
        if x in group:
            found = True   # 영역: 'helper' -- 좋지 않음!
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


print("Example 7")
def sort_priority3(numbers, group):
    found = False

    def helper(x):
        nonlocal found  # 추가함
        if x in group:
            found = True
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


print("Example 8")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority3(numbers, group)
print("찾음:", found)
print(numbers)


print("Example 9")
class Sorter:
    def __init__(self, group):  
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)


print("Example 10")
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
sorter = Sorter(group)
numbers.sort(key=sorter)
print("찾음:", sorter.found)
print(numbers)
