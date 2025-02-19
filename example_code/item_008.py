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
fresh_fruit = {
    "사과": 10,
    "바나나": 8,
    "레몬": 5,
}


print("Example 2")
def make_lemonade(count):
    print(f"{count} 레몬을 레모네이드로 만듭니다")

def out_of_stock():
    print("Out of stock!")

count = fresh_fruit.get("레몬", 0)
if count:
    make_lemonade(count)
else:
    out_of_stock()


print("Example 3")
if count := fresh_fruit.get("레몬", 0):
    make_lemonade(count)
else:
    out_of_stock()


print("Example 4")
def make_cider(count):
    print(f"{count} 사과를 사과주스로 만듭니다")

count = fresh_fruit.get("사과", 0)
if count >= 4:
    make_cider(count)
else:
    out_of_stock()


print("Example 5")
if (count := fresh_fruit.get("사과", 0)) >= 4:
    make_cider(count)
else:
    out_of_stock()


print("Example 6")
def slice_bananas(count):
    print(f"{count} 바나나를 슬라이스합니다")
    return count * 4

class OutOfBananas(Exception):
    pass

def make_smoothies(count):
    print(f"{count} 바나나 슬라이스를 스무디로 만듭니다")

pieces = 0
count = fresh_fruit.get("banana", 0)
if count >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


print("Example 7")
count = fresh_fruit.get("banana", 0)
if count >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0  # 옮겨짐

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


print("Example 8")
pieces = 0
if (count := fresh_fruit.get("바나나", 0)) >= 2:  # 변경됨
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


print("Example 9")
if (count := fresh_fruit.get("바나나", 0)) >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0  # Moved

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


print("Example 10")
count = fresh_fruit.get("바나나", 0)
if count >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get("사과", 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get("레몬", 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = "없음"


print("Example 11")
if (count := fresh_fruit.get("바나나", 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get("사과", 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get("레몬", 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = "없음"


print("Example 12")
FRUIT_TO_PICK = [
    {"사과": 1, "바나나": 3},
    {"레몬": 2, "라임": 5},
    {"오렌지": 3, "멜론": 2},
]

def pick_fruit():
    if FRUIT_TO_PICK:
        return FRUIT_TO_PICK.pop(0)
    else:
        return []

def make_juice(fruit, count):
    return [(fruit, count)]

bottles = []
fresh_fruit = pick_fruit()
while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()

print(bottles)


print("Example 13")
FRUIT_TO_PICK = [
    {"사과": 1, "바나나": 3},
    {"레몬": 2, "라임": 5},
    {"오렌지": 3, "멜론": 2},
]
bottles = []
while True:                     # 루프
    fresh_fruit = pick_fruit()
    if not fresh_fruit:         # 중간에서 끝내기
        break
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)


print("Example 14")
FRUIT_TO_PICK = [
    {"사과": 1, "바나나": 3},
    {"레몬": 2, "라임": 5},
    {"오렌지": 3, "멜론": 2},
]

bottles = []
while fresh_fruit := pick_fruit():  # 변경됨
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)
