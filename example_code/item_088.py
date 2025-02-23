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
try:
    my_dict = {}
    my_dict["존재하지_않는_키"]
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 2")
my_dict = {}
try:
    my_dict["존재하지_않는_키"]
except KeyError:
    print("키를 찾을 수 없음!")


print("Example 3")
try:
    class MissingError(Exception):
        pass
    
    try:
        my_dict["존재하지_않는_키"]    # 첫 번째 예외 발생
    except KeyError:
        raise MissingError("이런!")  # 두 번째 예외 발생
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 4")
try:
    try:
        my_dict["존재하지_않는_키"]
    except KeyError:
        raise MissingError("이런!")
except MissingError as e:
    print("Second:", repr(e))
    print("First: ", repr(e.__context__))


print("Example 5")
def lookup(my_key):
    try:
        return my_dict[my_key]
    except KeyError:
        raise MissingError


print("Example 6")
my_dict["내 키 1"] = 123
print(lookup("내 키 1"))


print("Example 7")
try:
    print(lookup("내 키 2"))
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 8")
def contact_server(my_key):
    print(f"서버에서 {my_key!r} 검색")
    return "내 값 2"

def lookup(my_key):
    try:
        return my_dict[my_key]
    except KeyError:
        result = contact_server(my_key)
        my_dict[my_key] = result  # 로컬 캐시를 채운다
        return result


print("Example 9")
print("호출 1")
print("결과:", lookup("내 키 2"))
print("호출 2")
print("결과:", lookup("내 키 2"))


print("Example 10")
class ServerMissingKeyError(Exception):
    pass

def contact_server(my_key):
    print(f"서버에서 {my_key!r} 검색")
    raise ServerMissingKeyError


print("Example 11")
try:
    print(lookup("내 키 3"))
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 12")
def lookup(my_key):
    try:
        return my_dict[my_key]
    except KeyError:
        try:
            result = contact_server(my_key)
        except ServerMissingKeyError:
            raise MissingError        # 서버 오류를 변환
        else:
            my_dict[my_key] = result  # 로컬 캐시 채우기
            return result


print("Example 13")
try:
    print(lookup("내 키 4"))
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 14")
def lookup_explicit(my_key):
    try:
        return my_dict[my_key]
    except KeyError as e:              # Changed
        try:
            result = contact_server(my_key)
        except ServerMissingKeyError:
            raise MissingError from e  # Changed
        else:
            my_dict[my_key] = result
            return result


print("Example 15")
try:
    print(lookup_explicit("내 키 5"))
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 16")
try:
    lookup_explicit("내 키 6")
except Exception as e:
    print("Exception:", repr(e))
    print("Context:  ", repr(e.__context__))
    print("Cause:    ", repr(e.__cause__))
    print("Suppress: ", repr(e.__suppress_context__))


print("Example 17")
import traceback

try:
    lookup("내 키 7")
except Exception as e:
    stack = traceback.extract_tb(e.__traceback__)
    for frame in stack:
        print(frame.line)


print("Example 18")
def get_cause(exc):
    if exc.__cause__ is not None:
        return exc.__cause__
    elif not exc.__suppress_context__:
        return exc.__context__
    else:
        return None


print("Example 19")
try:
    lookup("내 키 8")
except Exception as e:
    while e is not None:
        stack = traceback.extract_tb(e.__traceback__)
        for i, frame in enumerate(stack, 1):
            print(i, frame.line)
        e = get_cause(e)
        if e:
            print("발생 원인:")


print("Example 20")
def contact_server(key):
    raise ServerMissingKeyError from None  # 원인이 되는 예외 무시


print("Example 21")
try:
    print(lookup("내 키 9"))
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False
