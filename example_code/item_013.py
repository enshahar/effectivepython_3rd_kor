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

print("아이템 13")
print("Example 1")
my_test1 = "hello" "아름다운" "world"
my_test2 = "hello" + "아름다운" + "world"
assert my_test1 == my_test2


print("Example 2")
x = 1
my_test1 = (
    r"첫번째 \ 부분은 이스케이프(escapes)가 있음\n, "
    f"여기서는 문자열 인터폴레이션 {x}이 들어있음, "
    '여기에는 "큰 따옴표" 문자열이 들어있음'
)
print(my_test1)


print("Example 3")
y = 2
my_test2 = r"fir\st" f"{y}" '"third"'
print(my_test2)


print("Example 4")
my_test3 = r"fir\st", f"{y}" '"third"'
print(my_test3)


print("Example 5")
my_test4 = [
    "first line\n",
    "두번째 줄\n",
    "third line\n",
]
print(my_test4)


print("Example 6")
my_test5 = [
    "first line\n",
    "두번째 줄\n"  # 쉼표를 제거함
    "third line\n",
]
print(my_test5)


print("Example 7")
my_test5 = [
    "first line\n",
    "두번째 줄\n" "third line\n",
]


print("Example 8")
my_test6 = [
    "first line\n",
    "두번째 줄\n" +  # 명시적 결합
    "third line\n",
]
assert my_test5 == my_test6


print("Example 9")
my_test6 = [
    "first line\n",
    "두번째 줄\n" + "third line\n",
]


print("Example 10")
print("this is my long message(긴 메시지) "
      "that should be printed out")


print("Example 11")
import sys

print("this is my long message(긴 메시지) "
      "that should be printed out",
      end="",
      file=sys.stderr)


print("Example 12")
import sys

first_value = ...
second_value = ...

class MyData:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

value = MyData(123,
               first_value,
               f"my format string {x}"
               f"다른 값 {y}",
               "and here is more text",
               second_value,
               stream=sys.stderr)


print("Example 13")
value2 = MyData(123,
                first_value,
                f"my format string {x}" +  # 명시적 연결
                f"다른 값 {y}",
                "and here is more text",
                second_value,
                stream=sys.stderr)
