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
counters = {
    "펌퍼니클": 2,
    "사워도": 1,
}


print("Example 2")
key = "밀"

if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1
print(counters)


print("Example 3")
key = "브리오슈"

try:
    count = counters[key]
except KeyError:
    count = 0

counters[key] = count + 1

print(counters)


print("Example 4")
key = "통곡물"

count = counters.get(key, 0)
counters[key] = count + 1

print(counters)


print("Example 5")
key = "바게트"

if key not in counters:
    counters[key] = 0
counters[key] += 1

key = "치아바타"

if key in counters:
    counters[key] += 1
else:
    counters[key] = 1

key = "치아바타"

try:
    counters[key] += 1
except KeyError:
    counters[key] = 1

print(counters)


print("Example 6")
votes = {
    "바게트": ["현석", "계영"],
    "치아바타": ["성원", "정원"],
}

key = "브리오슈"
who = "혜원"

if key in votes:
    names = votes[key]
else:
    votes[key] = names = []

names.append(who)
print(votes)


print("Example 7")
key = "호밀"
who = "유진"

try:
    names = votes[key]
except KeyError:
    votes[key] = names = []

names.append(who)

print(votes)


print("Example 8")
key = "밀"
who = "삼현"

names = votes.get(key)
if names is None:
    votes[key] = names = []

names.append(who)

print(votes)


print("Example 9")
key = "브리오슈"
who = "계원"

if (names := votes.get(key)) is None:
    votes[key] = names = []

names.append(who)

print(votes)


print("Example 10")
key = "옥수수빵"
who = "영무"

names = votes.setdefault(key, [])
names.append(who)

print(votes)


print("Example 11")
data = {}
key = "foo"
value = []
data.setdefault(key, value)
print("이전:", data)
value.append("hello")
print("이후: ", data)


print("Example 12")
key = "호랑이빵"

count = counters.setdefault(key, 0)
counters[key] = count + 1

print(counters)
