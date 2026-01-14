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


print("아이템 124")
print("Example 2")
# 다음 명령으로 이 파일의 타입을 체크하세요: python3 -m mypy <path>

def subtract(a: int, b: int) -> int:  # 함수에 타입 애너테이션을 붙임
    return a - b

subtract(10, "5")  # 아차! 문자열 값을 넘김
