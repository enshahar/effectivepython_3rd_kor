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

print("아이템 7")
print("Example 1")
i = 3
x = "짝수" if i % 2 == 0 else "홀수"
print(x)


print("Example 2")
def fail():
    raise Exception("이런!")

x = fail() if False else 20
print(x)


print("Example 3")
result = [x / 4 for x in range(10) if x % 2 == 0]
print(result)


print("Example 4")
x = (i % 2 == 0 and "짝수") or "홀수"


print("Example 5")
if i % 2 == 0:
    x = "짝수"
else:
    x = "홀수"


print("Example 6")
if i % 2 == 0:
    x = "짝수"
    print("짝수였음!")  # 추가됨
else:
    x = "홀수"


print("Example 7")
if i % 2 == 0:
    x = "짝수"
elif i % 3 == 0:  # 추가됨
    x = "3으로 나눠짐"
else:
    x = "홀수"


print("Example 8")
def number_group(i):
    if i % 2 == 0:
        return "짝수"
    else:
        return "홀수"

x = number_group(i)  # 짧은 호출
print(x)


print("Example 9")
def my_long_function_call(*args):
    pass

def my_other_long_function_call(*args):
    pass


x = (my_long_function_call(1, 2, 3) if i % 2 == 0
     else my_other_long_function_call(4, 5, 6))


print("Example 10")
x = (
    my_long_function_call(1, 2, 3)
    if i % 2 == 0
    else my_other_long_function_call(4, 5, 6)
)


print("Example 11")
x = 2
y = 1

if x and (z := x > y):
    pass


print("Example 12")
try:
    # 컴파일되지 않음
    source = """if x and z := x > y:
        pass"""
    eval(source)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 13")
if x > y if z else w:    # 모호함
    pass

if x > (y if z else w):  # 명확함
    pass


print("Example 14")
z = dict(
    your_value=(y := 1),
)


print("Example 15")
try:
    # 컴파일되지 않음
    source = """w = dict(
        other_value=y := 1,
    )      """
    eval(source)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 16")
v = dict(
    my_value=1 if x else 3,
)
