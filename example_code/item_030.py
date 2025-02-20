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
def my_func(items):
    items.append(4)

x = [1, 2, 3]
my_func(x)
print(x)  # 이제 리스트에 4가 포함됨


print("Example 2")
a = [7, 6, 5]
b = a          # 별명 생성
my_func(b)
print(a)       # 이제 리스트에 4가 포함됨


print("Example 3")
def capitalize_items(items):
    for i in range(len(items)):
        items[i] = items[i].capitalize()

my_items = ["hello", "world"]
items_copy = my_items[:]  # 복사본 생성
capitalize_items(items_copy)
print(items_copy)


print("Example 4")
def concat_pairs(items):
    for key in items:
        items[key] = f"{key}={items[key]}"

my_pairs = {"foo": 1, "bar": 2}
pairs_copy = my_pairs.copy()  # 복사본 생성
concat_pairs(pairs_copy)
print(pairs_copy)


print("Example 5")
class MyClass:
    def __init__(self, value):
        self.value = value

x = MyClass(10)

def my_func(obj):
    obj.value = 20  # 객체를 수정함

my_func(x)
print(x.value)
