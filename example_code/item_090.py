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

print("아이템 90")
print("Example 1")
try:
    n = 3
    assert n % 2 == 0, f"{n=}은 짝수 아님"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 2")
try:
    if __debug__:
        if not (n % 2 == 0):
            raise AssertionError(f"{n=}은 짝수 아님")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 3")
try:
    def expensive_check(x):
        return x != 2
    
    items = [1, 2, 3]
    if __debug__:
        for i in items:
            assert expensive_check(i), f"실패함 {i=}"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 4")
try:
    # 컴파일되지 않음
    source = """__debug__ = False"""
    eval(source)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False
