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

# global_lock_perf.py
import timeit
import threading

trials = 100_000_000

initialized = False
initialized_lock = threading.Lock()

result = timeit.timeit(
    stmt="""
global initialized
# 잠금 없이 사전 검사
if not initialized:
    with initialized_lock:
        # 잠금을 획득한 후 다시 확인
        if not initialized:
            # 비용이 큰 초기화 작업 실행
            initialized = True
""",
    globals=globals(),
    number=trials,
)

print(f"{result/trials * 1e9:2.1f} 나노초/호출")
