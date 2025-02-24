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
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)


print("Example 2")
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f"Tool({self.name!r}, {self.weight})"

tools = [
    Tool("수평기", 3.5),
    Tool("망치", 1.25),
    Tool("십자드라이버", 0.5),
    Tool("치즐", 0.25),
]


print("Example 3")
try:
    tools.sort()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 4")
print("정렬전:", repr(tools))
tools.sort(key=lambda x: x.name)
print("\n정렬후:  ", tools)


print("Example 5")
tools.sort(key=lambda x: x.weight)
print("무게로 정렬:", tools)


print("Example 6")
places = ["home", "work", "New York", "Paris"]
places.sort()
print("대소문자 구분:    ", places)
places.sort(key=lambda x: x.lower())
print("대소문자 구분없음:", places)


print("Example 7")
power_tools = [
    Tool("드릴", 4),
    Tool("원형 톱", 5),
    Tool("착암기", 40),
    Tool("연마기", 4),
]


print("Example 8")
saw = (5, "원형 톱")
jackhammer = (40, "착암기")
assert not (jackhammer < saw)  # 예상한 대로 결과가 나온다


print("Example 9")
drill = (4, "드릴")
sander = (4, "연마기")
assert drill[0] == sander[0]  # 무게가 같다
assert drill[1] < sander[1]   # 알파벳순으로 볼 때 더 작다
assert drill < sander         # 그러므로 drill이 더 먼저다


print("Example 10")
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)


print("Example 11")
power_tools.sort(
    key=lambda x: (x.weight, x.name),
    reverse=True,  # 모든 비교 기준을 내림차순으로 만든다
)
print(power_tools)


print("Example 12")
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)


print("Example 13")
try:
    power_tools.sort(key=lambda x: (x.weight, -x.name), reverse=True)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 14")
power_tools.sort(
    key=lambda x: x.name,    # name 기준 오름차순
)
power_tools.sort(
    key=lambda x: x.weight,  # weight 기준 내림차순
    reverse=True,
)
print(power_tools)


print("Example 15")
power_tools.sort(key=lambda x: x.name)
print(power_tools)


print("Example 16")
power_tools.sort(
    key=lambda x: x.weight,
    reverse=True,
)
print(power_tools)
