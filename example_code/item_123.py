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
def print_distance(speed, duration):
    distance = speed * duration
    print(f"{distance} miles")

print_distance(5, 2.5)


print("Example 2")
print_distance(1000, 3)


print("Example 3")
CONVERSIONS = {
    "mph": 1.60934 / 3600 * 1000,  # m/s
    "hours": 3600,                 # seconds
    "miles": 1.60934 * 1000,       # m
    "meters": 1,                   # m
    "m/s": 1,                      # m/s
    "seconds": 1,                  # s
}

def convert(value, units):
    rate = CONVERSIONS[units]
    return rate * value

def localize(value, units):
    rate = CONVERSIONS[units]
    return value / rate

def print_distance(
    speed,
    duration,
    *,
    speed_units="mph",
    time_units="hours",
    distance_units="miles",
):
    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f"{distance} {distance_units}")


print("Example 4")
print_distance(
    1000,
    3,
    speed_units="meters",
    time_units="seconds",
)


print("Example 5")
import warnings

def print_distance(
    speed,
    duration,
    *,
    speed_units=None,
    time_units=None,
    distance_units=None,
):
    if speed_units is None:
        warnings.warn(
            "speed_units가 필요합니다",
            DeprecationWarning,
        )
        speed_units = "mph"

    if time_units is None:
        warnings.warn(
            "time_units가 필요합니다",
            DeprecationWarning,
        )
        time_units = "hours"

    if distance_units is None:
        warnings.warn(
            "distance_units가 필요합니다",
            DeprecationWarning,
        )
        distance_units = "miles"

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f"{distance} {distance_units}")


print("Example 6")
import contextlib
import io

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    print_distance(
        1000,
        3,
        speed_units="meters",
        time_units="seconds",
    )

print(fake_stderr.getvalue())


print("Example 7")
def require(name, value, default):
    if value is not None:
        return value
    warnings.warn(
        f"{name}이 필수로 될 예정입니다. 코드를 변경해 주세요",
        DeprecationWarning,
        stacklevel=3,
    )
    return default

def print_distance(
    speed,
    duration,
    *,
    speed_units=None,
    time_units=None,
    distance_units=None,
):
    speed_units = require(
        "speed_units",
        speed_units,
        "mph",
    )
    time_units = require(
        "time_units",
        time_units,
        "hours",
    )
    distance_units = require(
        "distance_units",
        distance_units,
        "miles",
    )

    norm_speed = convert(speed, speed_units)
    norm_duration = convert(duration, time_units)
    norm_distance = norm_speed * norm_duration
    distance = localize(norm_distance, distance_units)
    print(f"{distance} {distance_units}")


print("Example 8")
import contextlib
import io

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    print_distance(
        1000,
        3,
        speed_units="meters",
        time_units="seconds",
    )

print(fake_stderr.getvalue())


print("Example 9")
warnings.simplefilter("error")
try:
    warnings.warn(
        "이 사용법은 앞으로 금지될 예정입니다",
        DeprecationWarning,
    )
except DeprecationWarning:
    pass  # 예외가 발생하리라 예상함
else:
    assert False

warnings.resetwarnings()


print("Example 10")
warnings.resetwarnings()

warnings.simplefilter("ignore")
warnings.warn("stderr에 출력되지 않음")

warnings.resetwarnings()


print("Example 11")
import logging

fake_stderr = io.StringIO()
handler = logging.StreamHandler(fake_stderr)
formatter = logging.Formatter("%(asctime)-15s WARNING] %(message)s")
handler.setFormatter(formatter)

logging.captureWarnings(True)
logger = logging.getLogger("py.warnings")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

warnings.resetwarnings()
warnings.simplefilter("default")
warnings.warn("로그 출력에 표시됨")

print(fake_stderr.getvalue())

warnings.resetwarnings()


print("Example 12")
with warnings.catch_warnings(record=True) as found_warnings:
    found = require("my_arg", None, "fake units")
    expected = "fake units"
    assert found == expected


print("Example 13")
assert len(found_warnings) == 1
single_warning = found_warnings[0]
assert str(single_warning.message) == (
    "my_arg이 필수로 될 예정입니다. 코드를 변경해 주세요"
)
assert single_warning.category == DeprecationWarning
