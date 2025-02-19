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
def take_action(light):
    if light == "빨강":
        print("Stop")
    elif light == "노랑":
        print("속도를 줄이자")
    elif light == "초록":
        print("가자!")
    else:
        raise RuntimeError


print("Example 2")
take_action("빨강")
take_action("노랑")
take_action("초록")


print("Example 3")
def take_match_action(light):
    match light:
        case "빨강":
            print("멈추자")
        case "노랑":
            print("속도를 줄이자")
        case "초록":
            print("가자!")
        case _:
            raise RuntimeError


take_match_action("빨강")
take_match_action("노랑")
take_match_action("초록")


print("Example 4")
try:
    # 컴파일되지 않음
    source = """# Added these constants
    RED = "빨강"
    YELLOW = "노랑"
    GREEN = "초록"
    
    def take_constant_action(light):
        match light:
            case RED:               # 변경함
                print("멈추자")
            case YELLOW:            # 변경함
                print("속도를 줄이자")
            case GREEN:             # 변경함
                print("가자!")
            case _:
                raise RuntimeError"""
    eval(source)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
RED = "빨강"
YELLOW = "노랑"
GREEN = "초록"

def take_truncated_action(light):
    match light:
        case RED:
            print("멈추자")


print("Example 6")
take_truncated_action(GREEN)


print("Example 7")
def take_debug_action(light):
    match light:
        case RED:
            print(f"{RED=}, {light=}")

take_debug_action(GREEN)


print("Example 8")
def take_unpacking_action(light):
    try:
        (RED,) = (light,)
    except TypeError:
        # 매치되지 않음
        pass
    else:
        # 매치됨
        print(f"{RED=}, {light=}")


take_unpacking_action(GREEN)


print("Example 9")
import enum                     # 추가됨

class ColorEnum(enum.Enum):     # 추가됨
    RED = "빨강"
    YELLOW = "노랑"
    GREEN = "초록"

def take_enum_action(light):
    match light:
        case ColorEnum.RED:     # 변경함
            print("멈추자")
        case ColorEnum.YELLOW:  # 변경함
            print("속도를 줄이자")
        case ColorEnum.GREEN:   # 변경함
            print("가자!")
        case _:
            raise RuntimeError

take_enum_action(ColorEnum.RED)
take_enum_action(ColorEnum.YELLOW)
take_enum_action(ColorEnum.GREEN)


print("Example 10")
for index, value in enumerate("abc"):
    print(f"인덱스 {index}는 {value}")


print("Example 11")
my_tree = (10, (7, None, 9), (13, 11, None))


print("Example 12")
def contains(tree, value):
    if not isinstance(tree, tuple):
        return tree == value

    pivot, left, right = tree

    if value < pivot:
        return contains(left, value)
    elif value > pivot:
        return contains(right, value)
    else:
        return value == pivot


print("Example 13")
assert contains(my_tree, 9)
assert not contains(my_tree, 14)

for i in range(0, 14):
    print(i, contains(my_tree, i))


print("Example 14")
def contains_match(tree, value):
    match tree:
        case pivot, left, _ if value < pivot:
            return contains_match(left, value)
        case pivot, _, right if value > pivot:
            return contains_match(right, value)
        case (pivot, _, _) | pivot:
            return pivot == value


assert contains_match(my_tree, 9)
assert not contains_match(my_tree, 14)

for i in range(0, 14):
    print(i, contains_match(my_tree, i))


print("Example 15")
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


print("Example 16")
obj_tree = Node(
    value=10,
    left=Node(value=7, right=9),
    right=Node(value=13, left=11),
)


print("Example 17")
def contains_class(tree, value):
    if not isinstance(tree, Node):
        return tree == value
    elif value < tree.value:
        return contains_class(tree.left, value)
    elif value > tree.value:
        return contains_class(tree.right, value)
    else:
        return tree.value == value


assert contains_class(obj_tree, 9)
assert not contains_class(obj_tree, 14)

for i in range(0, 14):
    print(i, contains_class(obj_tree, i))


print("Example 18")
def contains_match_class(tree, value):
    match tree:
        case Node(value=pivot, left=left) if value < pivot:
            return contains_match_class(left, value)
        case Node(value=pivot, right=right) if value > pivot:
            return contains_match_class(right, value)
        case Node(value=pivot) | pivot:
            return pivot == value


assert contains_match_class(obj_tree, 9)
assert not contains_match_class(obj_tree, 14)

for i in range(0, 14):
    print(i, contains_match_class(obj_tree, i))


print("Example 19")
record1 = """{"customer": {"last": "아", "first": "이유"}}"""
record2 = """{"customer": {"entity": "멋진 음악사"}}"""


print("Example 20")
from dataclasses import dataclass

@dataclass
class PersonCustomer:
    first_name: str
    last_name: str

@dataclass
class BusinessCustomer:
    company_name: str


print("Example 21")
import json

def deserialize(data):
    record = json.loads(data)
    match record:
        case {"customer": {"last": last_name, "first": first_name}}:
            return PersonCustomer(first_name, last_name)
        case {"customer": {"entity": company_name}}:
            return BusinessCustomer(company_name)
        case _:
            raise ValueError("알 수 없는 레코드 타입")


print("Example 22")
print("레코드1:", deserialize(record1))
print("레코드2:", deserialize(record2))
