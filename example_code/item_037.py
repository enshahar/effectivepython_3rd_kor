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
def safe_division(
    number,
    divisor,
    ignore_overflow,
    ignore_zero_division,
):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


print("Example 2")
result = safe_division(1.0, 10**500, True, False)
print(result)


print("Example 3")
result = safe_division(1.0, 0, False, True)
print(result)


print("Example 4")
def safe_division_b(
    number,
    divisor,
    ignore_overflow=False,       # 변경함
    ignore_zero_division=False,  # 변경함
):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


print("Example 5")
result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)


print("Example 6")
assert safe_division_b(1.0, 10**500, True, False) == 0


print("Example 7")
def safe_division_c(
    number,
    divisor,
    *,  # 추가함
    ignore_overflow=False,
    ignore_zero_division=False,
):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


print("Example 8")
try:
    safe_division_c(1.0, 10**500, True, False)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 9")
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float("inf")

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass  # 예상대로 예외가 발생함
else:
    assert False


print("Example 10")
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4


print("Example 11")
def safe_division_d(
    numerator,    # 변경함
    denominator,  # 변경함
    *,
    ignore_overflow=False,
    ignore_zero_division=False
):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


print("Example 12")
try:
    safe_division_d(number=2, divisor=5)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 13")
def safe_division_e(
    numerator,
    denominator,
    /,  # 추가함
    *,
    ignore_overflow=False,
    ignore_zero_division=False,
):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


print("Example 14")
assert safe_division_e(2, 5) == 0.4


print("Example 15")
try:
    safe_division_e(numerator=2, denominator=5)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 16")
def safe_division_f(
    numerator,
    denominator,
    /,
    ndigits=10,  # 변경함
    *,
    ignore_overflow=False,
    ignore_zero_division=False,
):
    try:
        fraction = numerator / denominator  # 변경함
        return round(fraction, ndigits)     # 변경함
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


print("Example 17")
result = safe_division_f(22, 7)
print(result)

result = safe_division_f(22, 7, 5)
print(result)

result = safe_division_f(22, 7, ndigits=2)
print(result)
