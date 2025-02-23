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
import time

now = 1710047865.0
local_tuple = time.localtime(now)
time_format = "%Y-%m-%d %H:%M:%S"
time_str = time.strftime(time_format, local_tuple)
print(time_str)


print("Example 2")
time_tuple = time.strptime(time_str, time_format)
utc_now = time.mktime(time_tuple)
print(utc_now)


print("Example 3")
parse_format = "%Y-%m-%d %H:%M:%S %Z"
depart_icn = "2025-02-23 11:30:00 KST"
time_tuple = time.strptime(depart_icn, parse_format)
time_str = time.strftime(time_format, time_tuple)
print(time_str)


print("Example 4")
try:
    arrival_sfo = "2025-02-24 04:40:00 PDT"
    time_tuple = time.strptime(arrival_sfo, time_format)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
from datetime import datetime, timezone

now = datetime(2025, 2, 23, 11, 30, 0) # 시간대 설정이 안된 시간을 만듦
now_utc = now.replace(tzinfo=timezone.utc) # 시간대를 UTC로 강제 지정
now_local = now_utc.astimezone()           # UTC 시간을 디폴트 시간대로 변환
print(now_local)


print("Example 6")
time_str = "2025-02-23 20:30:00"
now = datetime.strptime(time_str, time_format) # 시간대 설정이 안된 시간으로 문자열을 구문분석
time_tuple = now.timetuple()         # 유닉스 시간 구조체로 변환
utc_now = time.mktime(time_tuple)    # 구조체로부터 유닉스 타임스탬프 생성
print(utc_now)

# 로컬 시간으로 변환해 시간이 일치하나 보기(책에는 없음)
print("Example 6 결과에서 로컬 시간 얻기")
local_tuple = time.localtime(utc_now)
time_format = "%Y-%m-%d %H:%M:%S"
time_str = time.strftime(time_format, local_tuple)
print(time_str)

print("Example 7")
from zoneinfo import ZoneInfo

arrival_sfo = "2025-02-24 04:40:00"
sfo_dt_naive = datetime.strptime(arrival_sfo, time_format)   # 시간대가 설정되지 않은 시간
pacific = ZoneInfo("US/Pacific")                             # 샌프란시스코의 시간대
sfo_dt = sfo_dt_naive.replace(tzinfo=pacific)                # 시간대를 샌프란시스코 시간대로 변경
utc_dt = sfo_dt.astimezone(timezone.utc)                     # UTC로 변경
print("PST: ",sfo_dt)
print("UTC: ",utc_dt)



print("Example 8")
korea = ZoneInfo("Asia/Seoul")
korea_dt = utc_dt.astimezone(korea)
print("KST:", korea_dt)


print("Example 9")
nepal = ZoneInfo("Asia/Katmandu")
nepal_dt = utc_dt.astimezone(nepal)
print("NPT:", nepal_dt)
