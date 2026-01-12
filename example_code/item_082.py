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

print("아이템 82")
print("Example 1")
from threading import Lock

lock = Lock()
with lock:
    # 어떤 불변 조건을 유지하면서 작업을 수행한다
    pass


print("Example 2")
lock.acquire()
try:
    # 어떤 불변 조건을 유지하면서 작업을 수행한다
    pass
finally:
    lock.release()


print("Example 3")
import logging

logging.getLogger().setLevel(logging.WARNING)

def my_function():
    logging.debug("디버깅 데이터")
    logging.error("오류 로그")
    logging.debug("추가 디버깅 데이터")

print("Example 4")
my_function()


print("Example 5")
from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


print("Example 6")
with debug_logging(logging.DEBUG):
    print("* 컨텍스트 내부:")
    my_function()

print("* 컨텍스트 이후:")
my_function()


print("Example 7")
with open("my_output.txt", "w") as handle:
    handle.write("데이터입니다!")


print("Example 8")
handle = open("my_output.txt", "w")
try:
    handle.write("데이터입니다!")
finally:
    handle.close()


print("Example 9")
@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


print("Example 10")
with log_level(logging.DEBUG, "my-log") as my_logger:
    # 영문판 소스코드에서는 로거 이름이 포함된 메시지를 만들어냈지만,
    # 애초 로그 함수가 로거 이름을 출력해 주기 때문에 중복임.
    # 이에 따라 한글판 소스코드에서는 메시지를 변경했음
    my_logger.debug(f"my_logger.debug() 호출")
    logging.debug("이 내용은 출력되지 않습니다")


print("Example 11")
logger = logging.getLogger("my-log")
logger.debug("디버깅 로그는 출력되지 않습니다")
logger.error("오류 로그는 출력됩니다")


print("Example 12")
with log_level(logging.DEBUG, "other-log") as my_logger:  # 변경함
    my_logger.debug(f"my_logger.debug() 호출")
    logging.debug("이 내용은 출력되지 않습니다")
