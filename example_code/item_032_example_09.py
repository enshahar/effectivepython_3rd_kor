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


print("아이템 32")
print("Example 9")
# Check types in this file with: python3 -m mypy <path>

def careful_divide(a: float, b: float) -> float:
    """ a를 b로 나눈다.

    Raises:
        ValueError: 입력을 나눌 수 없는 경우
    """
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("잘못된 입력")

try:
    result = careful_divide(1, 0)
except ValueError:
    print("잘못된 입력")  # 이 부분이 실행되리라 예상함
else:
    print(f"결과는 {result:.1f}")


assert careful_divide(1, 5) == 0.2
