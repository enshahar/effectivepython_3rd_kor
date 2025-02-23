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
def my_func():
    try:
        return 123
    finally:
        print("Finally my_func")

print("이전")
print(my_func())
print("이후")


print("Example 2")
def my_generator():
    try:
        yield 10
        yield 20
        yield 30
    finally:
        print("Finally my_generator")

print("이전")

for i in my_generator():
    print(i)

print("이후")


print("Example 3")
it = my_generator()
print("이전")
print(next(it))
print(next(it))
print("이후")


print("Example 4")
import gc

del it
gc.collect()


print("Example 5")
def catching_generator():
    try:
        yield 40
        yield 50
        yield 60
    except BaseException as e:  # GeneratorExit도 잡아냄
        print("핸들러가 잡아냄", type(e), e)
        raise


print("Example 6")
it = catching_generator()
print("이전")
print(next(it))
print(next(it))
print("이후")
del it
gc.collect()


print("Example 8")
with open("my_file.txt", "w") as f:
    for _ in range(20):
        f.write("a" * random.randint(0, 100))
        f.write("\n")

def lengths_path(path):
    try:
        with open(path) as handle:
            for i, line in enumerate(handle):
                print(f"줄 {i}")
                yield len(line.strip())
    finally:
        print("Finally lengths_path")


print("Example 9")
max_head = 0
it = lengths_path("my_file.txt")

for i, length in enumerate(it):
    if i == 5:
        break
    else:
        max_head = max(max_head, length)

print(max_head)


print("Example 10")
del it
gc.collect()


print("Example 11")
def lengths_handle(handle):
    try:
        for i, line in enumerate(handle):
            print(f"줄 {i}")
            yield len(line.strip())
    finally:
        print("Finally lengths_handle")


print("Example 12")
max_head = 0

with open("my_file.txt") as handle:
    it = lengths_handle(handle)
    for i, length in enumerate(it):
        if i == 5:
            break
        else:
            max_head = max(max_head, length)

print(max_head)
print("핸들 닫혔나:", handle.closed)
