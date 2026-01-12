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

print("아이템 15")
print("Example 1")
x = ["red", "orange", "yellow", "green", "blue", "purple"]
odds = x[::2]    # 1, 3, 5번째 (인덱스로는 0, 2, 4)
evens = x[1::2]  # 2, 4, 6번째 (인덱스로는 1, 3, 5)
print(odds)
print(evens)


print("Example 2")
x = b"mongoose"
y = x[::-1]
print(y)


print("Example 3")
x = "寿司"   # 초밥(스시)를 뜻하는 일본어 한자
y = x[::-1]
print(y)


print("Example 4")
try:
    w = "寿司"
    x = w.encode("utf-8")
    y = x[::-1]
    z = y.decode("utf-8")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
x = ["a", "b", "c", "d", "e", "f", "g", "h"]
x[::2]   # ["a", "c", "e", "g"]
x[::-2]  # ["h", "f", "d", "b"]
print(x[::2])
print(x[::-2])


print("Example 6")
x[2::2]     # ["c", "e", "g"]
x[-2::-2]   # ["g", "e", "c", "a"]
x[-2:2:-2]  # ["g", "e"]
x[2:2:-2]   # []
print(x[2::2])
print(x[-2::-2])
print(x[-2:2:-2])
print(x[2:2:-2])


print("Example 7")
y = x[::2]   # ["a", "c", "e", "g"]
z = y[1:-1]  # ["c", "e"]
print(x)
print(y)
print(z)

print("역주")
w = "abcZYX123"
x = w.encode("utf-8")
y = x[::-1]
z = y.decode("utf-8")
print(z)
