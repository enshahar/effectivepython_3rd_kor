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

import tracemalloc

tracemalloc.start(10)                      # 스택 깊이 설정
time1 = tracemalloc.take_snapshot()        # 이전 스냅샷

import waste_memory

x = waste_memory.run()                     # 디버깅할 코드
time2 = tracemalloc.take_snapshot()        # 이후 스냅샷

stats = time2.compare_to(time1, "lineno")  # 두 스냅샷을 비교
for stat in stats[:3]:
    print(stat)
