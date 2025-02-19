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
a = b"h\x65llo"
print(type(a))
print(list(a))
print(a)


print("Example 2")
a = "a\u0300 propos"
print(type(a))
print(list(a))
print(a)


print("Example 3")
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode("utf-8")
    else:
        value = bytes_or_str
    return value  # str 인스턴스

print(repr(to_str(b"foo")))
print(repr(to_str("bar")))
print(repr(to_str(b"\xed\x95\x9c"))) # UTF-8에서 한글은 3바이트임

print("Example 4")
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode("utf-8")
    else:
        value = bytes_or_str
    return value  # bytes 인스턴스

print(repr(to_bytes(b"foo")))
print(repr(to_bytes("bar")))
print(repr(to_bytes("한글")))


print("Example 5")
print(b"one" + b"two")
print("one" + "two")


print("Example 6")
try:
    b"one" + "two"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 7")
try:
    "one" + b"two"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
assert b"red" > b"blue"
assert "red" > "blue"


print("Example 9")
try:
    assert "red" > b"blue"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 10")
try:
    assert b"blue" < "red"
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 11")
print(b"foo" == "foo")


print("Example 12")
blue_bytes = b"blue"
blue_str = "blue"
print(b"red %s" % blue_bytes)
print("red %s" % blue_str)


print("Example 13")
try:
    print(b"red %s" % blue_str)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 14")
print("red %s" % blue_bytes)
print(f"red {blue_bytes}")


print("Example 15")
try:
    with open("data.bin", "w") as f:
        f.write(b"\xf1\xf2\xf3\xf4\xf5")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 16")
with open("data.bin", "wb") as f:
    f.write(b"\xf1\xf2\xf3\xf4\xf5")


print("Example 17")
try:
    # Silently force UTF-8 here to make sure this test fails on
    # all platforms. cp1252 considers these bytes valid on Windows.
    real_open = open
    
    def open(*args, **kwargs):
        kwargs["encoding"] = "utf-8"
        return real_open(*args, **kwargs)
    
    with open("data.bin", "r") as f:
        data = f.read()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 18")
# Restore the overloaded open above.
open = real_open
with open("data.bin", "rb") as f:
    data = f.read()
assert data == b"\xf1\xf2\xf3\xf4\xf5"


print("Example 19")
with open("data.bin", "r", encoding="cp1252") as f:
    data = f.read()
assert data == "ñòóôõ"
