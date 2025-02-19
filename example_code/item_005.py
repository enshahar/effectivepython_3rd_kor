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
no_snack = ()
snack = ("감자칩",)


print("Example 2")
snack_calories = {
    "감자칩": 140,
    "팝콘": 80,
    "땅콩": 190,
}
items = list(snack_calories.items())
print(items)


print("Example 3")
item = ("호박엿", "식혜")
first_item = item[0]   # 인덱스
first_half = item[:1]  # 슬라이스
print(first_item)
print(first_half)


print("Example 4")
try:
    pair = ("약과", "호박엿")
    pair[0] = "타래과"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
item = ("호박엿", "식혜")
first, second = item  # 언패킹
print(first, "과", second)


print("Example 6")
favorite_snacks = {
    "짭쪼름한 과자": ("프레즐", 100),
    "달콤한 과자": ("쿠키", 180),
    "채소": ("당근", 20),
}
((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()

print(f"제일 좋아하는 {type1}는 {name1}로, {cals1} 칼로리입니다.")
print(f"제일 좋아하는 {type2}는 {name2}로, {cals2} 칼로리입니다.")
print(f"제일 좋아하는 {type3}는 {name3}로, {cals3} 칼로리입니다.")


print("Example 7")
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i - 1]:
                temp = a[i]
                a[i] = a[i - 1]
                a[i - 1] = temp

names = ["프레즐", "당근", "쑥갓", "베이컨"]
bubble_sort(names)
print(names)


print("Example 8")
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i - 1]:
                a[i - 1], a[i] = a[i], a[i - 1]  # 맞바꾸기

names = ["프레즐", "당근", "쑥갓", "베이컨"]
bubble_sort(names)
print(names)


print("Example 9")
snacks = [("베이컨", 350), ("도넛", 240), ("머핀", 190)]
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f"#{i+1}: {name}은 {calories} 칼로리입니다.")


print("Example 10")
for rank, (name, calories) in enumerate(snacks, 1):
    print(f"#{rank}: {name}은 {calories} 칼로리입니다.")
