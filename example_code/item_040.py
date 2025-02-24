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
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)
print(squares)


print("Example 2")
squares = [x**2 for x in a]  # 리스트 컴프리헨션
print(squares)


print("Example 3")
alt = map(lambda x: x**2, a)
assert list(alt) == squares, f"{alt} {squares}"


print("Example 4")
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)


print("Example 5")
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)


print("Example 6")
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cubed_set)


print("Example 7")
alt_dict = dict(
    map(
        lambda x: (x, x**2),
        filter(lambda x: x % 2 == 0, a),
    )
)
alt_set = set(
    map(
        lambda x: x**3,
        filter(lambda x: x % 3 == 0, a),
    )
)
assert even_squares_dict == alt_dict
assert threes_cubed_set == alt_set
