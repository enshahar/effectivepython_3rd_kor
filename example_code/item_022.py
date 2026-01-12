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

print("아이템 22")
print("Example 1")
try:
    search_key = "빨강"
    my_dict = {"빨강": 1, "파랑": 2, "초록": 3}
    for key in my_dict:
        if key == "파랑":
            my_dict["노랑"] = 4  # 에러 발생
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 2")
try:
    my_dict = {"빨강": 1, "파랑": 2, "초록": 3}
    for key in my_dict:
        if key == "파랑":
            del my_dict["초록"]  # 에러 발생
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 3")
my_dict = {"빨강": 1, "파랑": 2, "초록": 3}
for key in my_dict:
    if key == "파랑":
        my_dict["초록"] = 4  # 정상
print(my_dict)


print("Example 4")
try:
    my_set = {"빨강", "파랑", "초록"}
    
    for color in my_set:
        if color == "파랑":
            my_set.add("노랑")  # 에러 발생
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
my_set = {"빨강", "파랑", "초록"}
for color in my_set:
    if color == "파랑":
        my_set.add("초록")  # 정상

print(my_set)


print("Example 6")
my_list = [1, 2, 3]

for number in my_list:
    print(number)
    if number == 2:
        my_list[0] = -1  # 정상

print(my_list)


print("Example 7")
my_list = [1, 2, 3]
bad_count = 0

for number in my_list:
    print(number)
    if number == 2:
        my_list.insert(0, 4)  # 에러 발생
    # 무한 루프에서 나가기
    bad_count += 1
    if bad_count > 5:
        print("...")
        break


print("Example 8")
my_list = [1, 2, 3]

for number in my_list:
    print(number)
    if number == 2:
        my_list.append(4)  # 이번에는 정상

print(my_list)


print("Example 9")
my_dict = {"빨강": 1, "파랑": 2, "초록": 3}

keys_copy = list(my_dict.keys())  # 복사
for key in keys_copy:             # 복사본을 순회
    if key == "파랑":
        my_dict["초록"] = 4        # 원본 딕셔너리를 변경

print(my_dict)


print("Example 10")
my_list = [1, 2, 3]

list_copy = list(my_list)     # 복사
for number in list_copy:      # 복사본을 순회
    print(number)
    if number == 2:
        my_list.insert(0, 4)  # 원본 리스트에 삽입

print(my_list)


print("Example 11")
my_set = {"빨강", "파랑", "초록"}

set_copy = set(my_set)        # 복사
for color in set_copy:        # 복사본을 이터레이션
    if color == "파랑":
        my_set.add("노랑")  # 원본 집합에 추가

print(my_set)


print("Example 12")
my_dict = {"빨강": 1, "파랑": 2, "초록": 3}
modifications = {}

for key in my_dict:
    if key == "파랑":
        modifications["초록"] = 4    # 스테이징 컨테이너에 추가

my_dict.update(modifications)       # 변경 사항 병합
print(my_dict)


print("Example 13")
my_dict = {"빨강": 1, "파랑": 2, "초록": 3}
modifications = {}

for key in my_dict:
    if key == "파랑":
        modifications["초록"] = 4
    value = my_dict[key]
    if value == 4:                   # 이 조건은 절대 참이 되지 않음
        modifications["노랑"] = 5

my_dict.update(modifications)        # 변경 사항 병합
print(my_dict)


print("Example 14")
my_dict = {"빨강": 1, "파랑": 2, "초록": 3}
modifications = {}

for key in my_dict:
    if key == "파랑":
        modifications["초록"] = 4
    value = my_dict[key]
    other_value = modifications.get(key)  # 캐시 확인
    if value == 4 or other_value == 4:
        modifications["노랑"] = 5

my_dict.update(modifications)             # 변경 사항 병합
print(my_dict)
