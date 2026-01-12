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

print("아이템 61")
print("Example 1")
class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f"{name}의 값"
        setattr(self, name, value)
        return value


print("Example 2")
data = LazyRecord()
print("이전:", data.__dict__)
print("foo: ", data.foo)
print("이후:", data.__dict__)


print("Example 3")
class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(
            f"* __getattr__({name!r}) 불림, "
            f"인스턴스 딕셔너리 채워 넣음"
        )
        result = super().__getattr__(name)
        print(f"* {result!r} 반환")
        return result

data = LoggingLazyRecord()
print("exists:    ", data.exists)
print("첫번째 foo:", data.foo)
print("두번째 foo:", data.foo)


print("Example 4")
class ValidatingRecord:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print(f"* __getattribute__({name!r}) 불림")
        try:
            value = super().__getattribute__(name)
            print(f"* {name!r} 찾음, {value!r} 반환")
            return value
        except AttributeError:
            value = f"{name}의 값"
            print(f"* {name!r}를 {value!r}로 설정")
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print("exists:    ", data.exists)
print("첫번째 foo:", data.foo)
print("두번째 foo:", data.foo)


print("Example 5")
try:
    class MissingPropertyRecord:
        def __getattr__(self, name):
            if name == "bad_name":
                raise AttributeError(f"{name} 없음")
            value = f"{name}의 값"
            setattr(self, name, value)
            return value
    
    data = MissingPropertyRecord()
    assert data.foo == "foo의 값"  # Test this works
    data.bad_name
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 6")
data = LoggingLazyRecord()  # __getattr__을 구현
print("이전:      ", data.__dict__)
print("첫번째 foo:", hasattr(data, "foo"))
print("이후:      ", data.__dict__)
print("두번째 foo:", hasattr(data, "foo"))


print("Example 7")
data = ValidatingRecord()  # __getattribute__를 구현
print("첫번째 foo:", hasattr(data, "foo"))
print("두번째 foo:", hasattr(data, "foo"))


print("Example 8")
class SavingRecord:
    def __setattr__(self, name, value):
        # 데이터를 데이터베이스 레코드에 저장한다
        pass
        super().__setattr__(name, value)


print("Example 9")
class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f"* __setattr__({name!r}, {value!r}) 불림")
        super().__setattr__(name, value)

data = LoggingSavingRecord()
print("이전:", data.__dict__)
data.foo = 5
print("이후:", data.__dict__)
data.foo = 7
print("최종:", data.__dict__)


print("Example 10")
class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print(f"* __getattribute__({name!r}) 불림")
        return self._data[name]


print("Example 11")
try:
    import sys

    sys.setrecursionlimit(50)
    data = BrokenDictionaryRecord({"foo": 3})
    data.foo
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 12")
class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        # 예제 코드를 위해 이상한 isinstance() 상호작용을 방지함
        if name == "__class__":
            return DictionaryRecord
        print(f"* __getattribute__({name!r}) 불림")
        data_dict = super().__getattribute__("_data")
        return data_dict[name]

data = DictionaryRecord({"foo": 3})
print("foo: ", data.foo)
