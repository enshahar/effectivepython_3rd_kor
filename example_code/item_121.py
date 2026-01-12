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

print("아이템 121")
print("Example 1")
# my_module.py
def determine_weight(volume, density):
    if density <= 0:
        raise ValueError("density는 양수여야 함")


try:
    determine_weight(1, 0)
except ValueError:
    pass
else:
    assert False


print("Example 2")
# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class InvalidDensityError(Error):
    """There was a problem with a provided density value."""

class InvalidVolumeError(Error):
    """There was a problem with the provided weight value."""

def determine_weight(volume, density):
    if density < 0:
        raise InvalidDensityError("density는 양수여야 함")
    if volume < 0:
        raise InvalidVolumeError("volume은 양수여야 함")
    if volume == 0:
        density / volume


print("Example 3")
class my_module:
    Error = Error
    InvalidDensityError = InvalidDensityError

    @staticmethod
    def determine_weight(volume, density):
        if density < 0:
            raise InvalidDensityError("density는 양수여야 함")
        if volume < 0:
            raise InvalidVolumeError("volume은 양수여야 함")
        if volume == 0:
            density / volume

try:
    weight = my_module.determine_weight(1, -1)
except my_module.Error:
    logging.exception("예상못한 오류")
else:
    assert False


print("Example 4")
SENTINEL = object()
weight = SENTINEL
try:
    weight = my_module.determine_weight(-1, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception("호출하는 코드의 오류")
else:
    assert False

assert weight is SENTINEL


print("Example 5")
try:
    weight = SENTINEL
    try:
        weight = my_module.determine_weight(0, 1)
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception("호출하는 코드의 오류")
    except Exception:
        logging.exception("API 코드의 오류!")
        raise  # 예외를 호출하는 쪽으로 다시 던짐
    else:
        assert False
    
    assert weight == 0
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 6")
# my_module.py

class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""


def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError("density는 양수여야 함")


print("Example 7")
try:
    my_module.NegativeDensityError = NegativeDensityError
    my_module.determine_weight = determine_weight
    try:
        weight = my_module.determine_weight(1, -1)
    except my_module.NegativeDensityError:
        raise ValueError("0 또는 양수만 제공해야 함")
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error:
        logging.exception("호출하는 코드의 오류")
    except Exception:
        logging.exception("API 코드의 오류!")
        raise
    else:
        assert False
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class WeightError(Error):
    """Base-class for weight calculation errors."""

class VolumeError(Error):
    """Base-class for volume calculation errors."""

class DensityError(Error):
    """Base-class for density calculation errors."""
