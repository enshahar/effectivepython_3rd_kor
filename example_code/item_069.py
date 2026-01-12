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

print("아이템 69")
print("Example 1")
counter = 0

def read_sensor(sensor_index):
    # 센서 데이터를 반환하거나 예외를 발생시킨다
    # 현재 코드로는 여기서 실제 무슨 일이 발생하지는 않지만,
    # 블러킹 I/O가 벌어지는 장소가 여기다
    pass

def get_offset(data):
    # 항상 1 이상의 값을 반환한다
    return 1

def worker(sensor_index, how_many):
    global counter
    # 작업자들이 카운팅을 시작할 때 동기화할 수 있게 여기 장벽을 설정한다.
    # 장벽이 없으면 스레드 시작 부가 비용이 높기 때문에 경합 상태가 발생하기 힘들다.
    BARRIER.wait()
    for _ in range(how_many):
        data = read_sensor(sensor_index)
        # CPytho의 eval 루프가 GIL을 해제할지 검사하게 하려면
        # +=에 전달하는 값이 함수 호출 등 단순하지 않은 식이어야만 한다.
        # 최적화로 인해 이런 현상이 발생한다.
        # 참조: https://github.com/python/cpython/commit/4958f5d69dd2bf86866c43491caf72f774ddec97
        counter += get_offset(data)


print("Example 2")
from threading import Thread

how_many = 10**6
sensor_count = 4

from threading import Barrier

BARRIER = Barrier(sensor_count)

threads = []
for i in range(sensor_count):
    thread = Thread(target=worker, args=(i, how_many))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * sensor_count
print(f"카운터 값은 {expected}이어야 하며, 실제로 {counter} 임")


print("Example 3")
data = None
counter += get_offset(data)


print("Example 4")
value = counter
delta = get_offset(data)
result = value + delta
counter = result


print("Example 5")
data_a = None
data_b = None
# 스레드 A에서 실행
value_a = counter
delta_a = get_offset(data_a)
# 스레드 B로 컨텍스트 스위칭
value_b = counter
delta_b = get_offset(data_b)
result_b = value_b + delta_b
counter = result_b
# 다시 스레드 A로 컨텍스트 스위칭
result_a = value_a + delta_a
counter = result_a


print("Example 6")
from threading import Lock

counter = 0
counter_lock = Lock()

def locking_worker(sensor_index, how_many):
    global counter
    BARRIER.wait()
    for _ in range(how_many):
        data = read_sensor(sensor_index)
        with counter_lock:                  # 추가함
            counter += get_offset(data)


print("Example 7")
BARRIER = Barrier(sensor_count)

for i in range(sensor_count):
    thread = Thread(target=locking_worker, args=(i, how_many))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * sensor_count
print(f"카운터 값은 {expected}이어야 하며, 실제로 {counter} 임")
