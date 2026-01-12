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

print("아이템 59")
print("Example 1")
from datetime import datetime, timedelta

class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f"Bucket(quota={self.quota})"


bucket = Bucket(60)
print(bucket)


print("Example 2")
def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


print("Example 3")
def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False  # 새 주기가 시작됐는데 아직 버킷 할당량이 재설정되지 않았다
    if bucket.quota - amount < 0:
        return False  # 버킷의 가용 용량이 충분하지 못하다
    bucket.quota -= amount
    return True       # 버킷의 가용 용량이 충분하므로 필요한 분량을 사용한다


print("Example 4")
bucket = Bucket(60)
fill(bucket, 100)
print(bucket)


print("Example 5")
if deduct(bucket, 99):
    print("가용 용량이 99 이상이었음")
else:
    print("가용 용량이 99보다 작음")

print(bucket)


print("Example 6")
if deduct(bucket, 3):
    print("가용 용량이 3 이상이었음")
else:
    print("가용 용량이 3보다 작음")

print(bucket)


print("Example 7")
class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (
            f"NewBucket(max_quota={self.max_quota}, "
            f"quota_consumed={self.quota_consumed})"
        )


    print("Example 8")
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed


    print("Example 9")
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # 새로운 주기가 되고 가용 용량을 재설정하는 경우
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # 새로운 주기가 되고 가용 용량을 추가하는 경우
            self.max_quota = amount + self.quota_consumed
        else:
            # 어떤 주기 안에서 가용 용량을 소비하는 경우
            self.quota_consumed = delta


print("Example 10")
bucket = NewBucket(60)
print("초기   ", bucket)
fill(bucket, 100)
print("채운 후", bucket)

if deduct(bucket, 99):
    print("가용 용량이 99 이상이었음")
else:
    print("가용 용량이 99보다 작음")

print("현재   ", bucket)

if deduct(bucket, 3):
    print("가용 용량이 3 이상이었음")
else:
    print("가용 용량이 3보다 작음")

print("여전히 ", bucket)


print("Example 11")
bucket = NewBucket(6000)
assert bucket.max_quota == 0
assert bucket.quota_consumed == 0
assert bucket.quota == 0

fill(bucket, 100)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 0
assert bucket.quota == 100

assert deduct(bucket, 10)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 10
assert bucket.quota == 90

assert deduct(bucket, 20)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 30
assert bucket.quota == 70

fill(bucket, 50)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 30
assert bucket.quota == 120

assert deduct(bucket, 40)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

assert not deduct(bucket, 81)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

bucket.reset_time += bucket.period_delta - timedelta(1)
assert bucket.quota == 80
assert not deduct(bucket, 79)

fill(bucket, 1)
assert bucket.quota == 1
