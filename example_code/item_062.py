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
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        global print
        orig_print = print
        print(f"* {name}에 대해 {meta}.__new__ 실행")
        print("부모클래스:", bases)
        print = pprint
        print(class_dict)
        print = orig_print
        return type.__new__(meta, name, bases, class_dict)

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass


print("Example 2")
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Polygon 클래스의 하위 클래스만 검증한다
        if bases:
            if class_dict["sides"] < 3:
                raise ValueError("Polygon의 sides는 3 이상이어야 합니다")
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None  # 하위 클래스가 이 값을 꼭 지정해야 함

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

assert Triangle.interior_angles() == 180
assert Rectangle.interior_angles() == 360
assert Nonagon.interior_angles() == 1260


print("Example 3")
try:
    print("클래스 선언 이전")
    
    class Line(Polygon):
        print("sides 설정 이전")
        sides = 2
        print("sides 설정 이후")
    
    print("클래스 선언 이후")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 4")
class BetterPolygon:
    sides = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError("Polygon의 sides는 3 이상이어야 합니다")

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

assert Hexagon.interior_angles() == 720


print("Example 5")
try:
    print("클래스 선언 이전")
    
    class Point(BetterPolygon):
        sides = 1
    
    print("클래스 선언 이후")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 6")
class ValidateFilled(type):
    def __new__(meta, name, bases, class_dict):
        # Filled 클래스의 하위 클래스만 검증한다
        if bases:
            if class_dict["color"] not in ("red", "green"):
                raise ValueError("지원하지 않는 채워 넣기 색상입니다")
        return type.__new__(meta, name, bases, class_dict)

class Filled(metaclass=ValidateFilled):
    color = None  # 하위 클래스가 이 값을 꼭 지정해야 함


print("Example 7")
try:
    class RedPentagon(Filled, Polygon):
        color = "blue"
        sides = 5
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # 루트 클래스가 아닌 경우만 검증한다
        if not class_dict.get("is_root"):
            if class_dict["sides"] < 3:
                raise ValueError("Polygon의 sides는 3 이상이어야 합니다")
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None  # Must be specified by subclasses

class ValidateFilledPolygon(ValidatePolygon):
    def __new__(meta, name, bases, class_dict):
        # 루트 클래스가 아닌 경우만 검증한다
        if not class_dict.get("is_root"):
            if class_dict["color"] not in ("red", "green"):
                raise ValueError("지원하지 않는 채워 넣기 색상입니다")
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None  # 하위 클래스가 이 값을 꼭 지정해야 함


print("Example 9")
class GreenPentagon(FilledPolygon):
    color = "green"
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)


print("Example 10")
try:
    class OrangePentagon(FilledPolygon):
        color = "orange"
        sides = 5
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 11")
try:
    class RedLine(FilledPolygon):
        color = "red"
        sides = 2
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 12")
class Filled:
    color = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ("red", "green", "blue"):
            raise ValueError("지원하지 않는 채워 넣기 색상입니다")


print("Example 13")
class RedTriangle(Filled, BetterPolygon):
    color = "red"
    sides = 3

ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, BetterPolygon)


print("Example 14")
try:
    print("클래스 선언 이전")
    
    class BlueLine(Filled, BetterPolygon):
        color = "blue"
        sides = 2
    
    print("클래스 선언 이후")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 15")
try:
    print("클래스 선언 이전")
    
    class BeigeSquare(Filled, BetterPolygon):
        color = "beige"
        sides = 4
    
    print("클래스 선언 이후")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 16")
class Top:
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"{cls}의 Top")

class Left(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"{cls}의 Left")

class Right(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"{cls}의 Right")

class Bottom(Left, Right):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"{cls}의 Bottom")
