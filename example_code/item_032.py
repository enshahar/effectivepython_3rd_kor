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
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


assert careful_divide(4, 2) == 2
assert careful_divide(0, 1) == 0
assert careful_divide(3, 6) == 0.5
assert careful_divide(1, 0) == None


print("Example 2")
x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print("잘못된 입력")
else:
    print(f"결과는 {result:.1f}")


print("Example 3")
x, y = 0, 5
result = careful_divide(x, y)
if not result:               # 변경함
    print("잘못된 입력")  # 이 코드가 실행되는데, 실행되면 안된다!
else:
    assert False


print("Example 4")
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


assert careful_divide(4, 2) == (True, 2)
assert careful_divide(0, 1) == (True, 0)
assert careful_divide(3, 6) == (True, 0.5)
assert careful_divide(1, 0) == (False, None)


print("Example 5")
x, y = 5, 0
success, result = careful_divide(x, y)
if not success:
    print("잘못된 입력")


print("Example 6")
x, y = 5, 0
_, result = careful_divide(x, y)
if not result:
    print("잘못된 입력")


print("Example 7")
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("잘못된 입력")  # 변경함


print("Example 8")
x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print("잘못된 입력")
else:
    print(f"결과는 {result:.1f}")
