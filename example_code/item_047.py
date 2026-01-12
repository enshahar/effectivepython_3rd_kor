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

print("아이템 47")
print("Example 1")
try:
    class MyError(Exception):
        pass
    
    def my_generator():
        yield 1
        yield 2
        yield 3
    
    it = my_generator()
    print(next(it))                         # 1을 내놓음
    print(next(it))                         # 2을 내놓음
    print(it.throw(MyError("테스트 오류")))    # 예외 발생
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 2")
def my_generator():
    yield 1

    try:
        yield 2
    except MyError:
        print("MyError 발생!")
    else:
        yield 3

    yield 4

it = my_generator()
print(next(it))                         # 1을 내놓음
print(next(it))                         # 2를 내놓음
print(it.throw(MyError("테스트 오류")))    # 4를 내놓음


print("Example 3")
class Reset(Exception):
    pass

def timer(period):
    current = period
    while current:
        try:
            yield current
        except Reset:
            print("재설정")
            current = period
        else:
            current -= 1


print("Example 4")
ORIGINAL_RESETS = [
    False,
    False,
    False,
    True,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]
RESETS = ORIGINAL_RESETS[:]

def check_for_reset():
    # 외부 이벤트를 폴링한다
    return RESETS.pop(0)

def announce(remaining):
    print(f"{remaining} 틱 남음")

def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)

run()


print("Example 5")
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        print("재설정")
        self.current = self.period

    def tick(self):
        before = self.current
        self.current -= 1
        return before

    def __bool__(self):
        return self.current > 0


print("Example 6")
RESETS = ORIGINAL_RESETS[:]

def run():
    timer = Timer(4)
    while timer:
        if check_for_reset():
            timer.reset()

        announce(timer.tick())

run()
