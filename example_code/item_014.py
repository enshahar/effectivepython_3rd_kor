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
a = ["a", "b", "c", "d", "e", "f", "g", "h"]
print("중간 2개:   ", a[3:5])
print("마지막 제외:", a[1:7])


print("Example 2")
assert a[:5] == a[0:5]


print("Example 3")
assert a[5:] == a[5:len(a)]


print("Example 4")
print(a[:])
print(a[:5])
print(a[:-1])
print(a[4:])
print(a[-3:])
print(a[2:5])
print(a[2:-1])
print(a[-3:-1])


print("Example 5")
a[:]      # ["a", "b", "c", "d", "e", "f", "g", "h"]
a[:5]     # ["a", "b", "c", "d", "e"]
a[:-1]    # ["a", "b", "c", "d", "e", "f", "g"]
a[4:]     #                     ["e", "f", "g", "h"]
a[-3:]    #                          ["f", "g", "h"]
a[2:5]    #           ["c", "d", "e"]
a[2:-1]   #           ["c", "d", "e", "f", "g"]
a[-3:-1]  #                          ["f", "g"]


print("Example 6")
first_twenty_items = a[:20]
last_twenty_items = a[-20:]


print("Example 7")
try:
    a[20]
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
b = a[3:]
print("Before:   ", b)
b[1] = 99
print("After:    ", b)
print("No change:", a)


print("Example 9")
print("Before ", a)
a[2:7] = [99, 22, 14]
print("After  ", a)


print("Example 10")
print("Before ", a)
a[2:3] = [47, 11]
print("After  ", a)


print("Example 11")
b = a[:]
assert b == a and b is not a


print("Example 12")
b = a
print("Before a", a)
print("Before b", b)
a[:] = [101, 102, 103]
assert a is b             # 여전히 같은 리스트 객체임
print("After a ", a)      # 새로운 내용이 들어 있음
print("After b ", b)      # 같은 리스트 객체이기 때문에 a와 내용이 같음
