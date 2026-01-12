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


print("아이템 4")
print("Example 1")
from urllib.parse import parse_qs

my_values = parse_qs("적=5&청=0&녹=", keep_blank_values=True)
print(repr(my_values))


print("Example 2")
print("적:    ", my_values.get("적"))
print("녹:    ", my_values.get("녹"))
print("투명도:", my_values.get("투명도"))


print("Example 3")
# 질의 문자열: "적=5&청=0&녹="
red = my_values.get("적", [""])[0] or 0
green = my_values.get("녹", [""])[0] or 0
opacity = my_values.get("투명도", [""])[0] or 0
print(f"적:     {red!r}")
print(f"녹:     {green!r}")
print(f"투명도: {opacity!r}")


print("Example 4")
red = int(my_values.get("적", [""])[0] or 0)
green = int(my_values.get("녹", [""])[0] or 0)
opacity = int(my_values.get("투명도", [""])[0] or 0)
print(f"적:     {red!r}")
print(f"녹:     {green!r}")
print(f"투명도: {opacity!r}")


print("Example 5")
red_str = my_values.get("적", [""])
red = int(red_str[0]) if red_str[0] else 0
green_str = my_values.get("녹", [""])
green = int(green_str[0]) if green_str[0] else 0
opacity_str = my_values.get("투명도", [""])
opacity = int(opacity_str[0]) if opacity_str[0] else 0
print(f"적:     {red!r}")
print(f"녹:     {green!r}")
print(f"투명도: {opacity!r}")


print("Example 6")
green_str = my_values.get("녹", [""])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0
print(f"녹:     {green!r}")


print("Example 7")
def get_first_int(values, key, default=0):
    found = values.get(key, [""])
    if found[0]:
        return int(found[0])
    return default


print("Example 8")
green = get_first_int(my_values, "녹")
print(f"녹:     {green!r}")
