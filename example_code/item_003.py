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


print("아이템 3")
print("Example 1")
try:
    # 컴파일되지 않기 때문에 eval로 컴파일 안됨을 보임
    source = """if True  # 잘못된 구문
      print('hello')"""
    eval(source)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 2")
try:
    # 컴파일되지 않음
    source = """1.3j5  # 잘못된 수 리터럴"""
    eval(source)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


# 함수를 호출하기 전에는 오류가 발생하지 않음
print("Example 3")
def bad_reference():
    print(my_var)
    my_var = 123


print("Example 4")
try:
    bad_reference()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False

# 함수를 호출하기 전에는 오류가 발생하지 않고, x에 따라 결과가 달라짐
print("Example 5")
def sometimes_ok(x):
    if x:
        my_var = 123
    print(my_var)


print("Example 6")
sometimes_ok(True)


print("Example 7")
try:
    sometimes_ok(False)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False

# 함수를 호출하기 전에는 오류가 발생하지 않음
print("Example 8")
def bad_math():
    return 1 / 0


print("Example 9")
try:
    bad_math()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False
