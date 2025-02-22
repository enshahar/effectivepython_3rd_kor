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
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


print("Example 2")
foo = MyObject()
assert foo.public_field == 5


print("Example 3")
assert foo.get_private_field() == 10


print("Example 4")
try:
    foo.__private_field
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


print("Example 6")
try:
    class MyParentObject:
        def __init__(self):
            self.__private_field = 71
    
    class MyChildObject(MyParentObject):
        def get_private_field(self):
            return self.__private_field
    
    baz = MyChildObject()
    baz.get_private_field()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 7")
assert baz._MyParentObject__private_field == 71


print("Example 8")
print(baz.__dict__)


print("Example 9")
class MyStringClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyStringClass(5)
assert foo.get_value() == "5"


print("Example 10")
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass("5")
assert foo.get_value() == 5


print("Example 11")
class MyBaseClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())         # Updated

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)  # Not updated


print("Example 12")
try:
    foo = MyIntegerSubclass(5)
    foo.get_value()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 13")
class MyStringClass:
    def __init__(self, value):
        # 여기서 객체에게 사용자가 제공한 값을 저장한다.
        # 사용자가 제공하는 값은 문자열로 타입 변환이 가능해야 하며
        # 일단 한번 객체 내부에 설정되고 나면 불변 값으로 취급돼야 한다.
        self._value = value


    def get_value(self):
        return str(self._value)


class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return self._value

foo = MyIntegerSubclass(5)
assert foo.get_value() == 5


print("Example 14")
class ApiClass:
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = "hello"  # 충돌

a = Child()
print(f"{a.get()} 와 {a._value} 는 달라야만 한다")


print("Example 15")
class ApiClass:
    def __init__(self):
        self.__value = 5     # 밑줄 2개!

    def get(self):
        return self.__value  # 밑줄 2개!

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = "hello"  # 잘 됨!

a = Child()
print(f"{a.get()} 와 {a._value} 는 달라야만 한다")
