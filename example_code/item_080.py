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
def try_finally_example(filename):
    print("* 파일 열기")
    handle = open(filename, encoding="utf-8") # OSError 발생할 수 있음
    try:
        print("* 데이터 읽기")
        return handle.read()                  # UnicodeDecodeError 발생할 수 있음
    finally:
        print("* close() 호출")
        handle.close()                        # try블록이 실행된 다음에 항상 실행됨


print("Example 2")
try:
    filename = "random_data.txt"
    
    with open(filename, "wb") as f:
        f.write(b"\xf1\xf2\xf3\xf4\xf5")  # 잘못된 utf-8 코드
    
    data = try_finally_example(filename)
    # 아래 코드에 도달하지 못해야 한다
    import sys
    
    sys.exit(1)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 3")
try:
    try_finally_example("does_not_exist.txt")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 4")
import json

def load_json_key(data, key):
    try:
        print("* JSON 데이터 로딩")
        result_dict = json.loads(data)     # ValueError가 발생할 수 있음
    except ValueError as e:
        print("* ValueError 처리")
        raise KeyError(key) from e
    else:
        print("* 키 탐색")
        return result_dict[key]            # KeyError가 발생할 수 있음


print("Example 5")
assert load_json_key('{"foo": "bar"}', "foo") == "bar"


print("Example 6")
try:
    load_json_key('{"foo": bad payload', "foo")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 7")
try:
    load_json_key('{"foo": "bar"}', "존재하지 않음")
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
UNDEFINED = object()
DIE_IN_ELSE_BLOCK = False

def divide_json(path):
    print("* 파일 열기")
    handle = open(path, "r+")             # OSError가 발생할 수 있음
    try:
        print("* 데이터 읽기")
        data = handle.read()              # UnicodeDecodeError가 발생할 수 있음
        print("* JSON 데이터 로딩")
        op = json.loads(data)             # ValueError가 발생할 수 있음
        print("* 계산 수행")
        value = (
            op["numerator"] /
            op["denominator"])            # ZeroDivisionError가 발생할 수 있음
    except ZeroDivisionError:
        print("* ZeroDivisionError 처리")
        return UNDEFINED
    else:
        print("* 계산 쓰기")
        op["result"] = value
        result = json.dumps(op)
        handle.seek(0)                    # OSError가 발생할 수 있음
        if DIE_IN_ELSE_BLOCK:
            import errno
            import os

            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))
        handle.write(result)              # OSError가 발생할 수 있음
        return value
    finally:
        print("* close() 호출")
        handle.close()                    # 어떤 경우든 실행됨


print("Example 9")
temp_path = "random_data.json"

with open(temp_path, "w") as f:
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1


print("Example 10")
with open(temp_path, "w") as f:
    f.write('{"numerator": 1, "denominator": 0}')

assert divide_json(temp_path) is UNDEFINED


print("Example 11")
try:
    with open(temp_path, "w") as f:
        f.write('{"numerator": 1 bad data')
    
    divide_json(temp_path)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 12")
try:
    with open(temp_path, "w") as f:
        f.write('{"numerator": 1, "denominator": 10}')
    DIE_IN_ELSE_BLOCK = True
    
    divide_json(temp_path)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False
