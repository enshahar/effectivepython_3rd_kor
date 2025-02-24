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
pictures = {}
path = "profile_1234.png"

with open(path, "wb") as f:
    f.write(b"image data here 1234")

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, "a+b")
    except OSError:
        print(f"파일을 열 수 없음: {path}")
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)


print("Example 2")
# Examples using in and KeyError
pictures = {}
path = "profile_9991.png"

with open(path, "wb") as f:
    f.write(b"image data here 9991")

if path in pictures:
    handle = pictures[path]
else:
    try:
        handle = open(path, "a+b")
    except OSError:
        print(f"파일을 열 수 없음: {path}")
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)

pictures = {}
path = "profile_9922.png"

with open(path, "wb") as f:
    f.write(b"image data here 9991")

try:
    handle = pictures[path]
except KeyError:
    try:
        handle = open(path, "a+b")
    except OSError:
        print(f"파일을 열 수 없음: {path}")
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)


print("Example 3")
pictures = {}
path = "profile_9239.png"

with open(path, "wb") as f:
    f.write(b"image data here 9239")

try:
    handle = pictures.setdefault(path, open(path, "a+b"))
except OSError:
    print(f"파일을 열 수 없음: {path}")
    raise
else:
    handle.seek(0)
    image_data = handle.read()

print(pictures)
print(image_data)


print("Example 4")
try:
    path = "profile_4555.csv"
    
    with open(path, "wb") as f:
        f.write(b"image data here 9239")
    
    from collections import defaultdict
    
    def open_picture(profile_path):
        try:
            return open(profile_path, "a+b")
        except OSError:
            print(f"파일을 열 수 없음: {profile_path}")
            raise
    
    pictures = defaultdict(open_picture)
    handle = pictures[path]
    handle.seek(0)
    image_data = handle.read()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
path = "account_9090.csv"

with open(path, "wb") as f:
    f.write(b"image data here 9090")

def open_picture(profile_path):
    try:
        return open(profile_path, "a+b")
    except OSError:
        print(f"파일을 열 수 없음: {profile_path}")
        raise

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
print(pictures)
print(image_data)
