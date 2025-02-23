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



print("Example 6")
# Check types in this file with: python3 -m mypy <path>

class Counter:
    def __init__(self) -> None:
        self.value: int = 0  # 필드/변수 애너테이션

    def add(self, offset: int) -> None:
        value += offset      # 아차! "self."를 안 씀

    def get(self) -> int:
        self.value           # 아차! "return"을 안 씀

counter = Counter()
counter.add(5)
counter.add(3)
assert counter.get() == 8
