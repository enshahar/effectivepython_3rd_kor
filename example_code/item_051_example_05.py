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



print("Example 5")
# 이 파일의 타입을 이렇게 체크해 보세요: python3 -m mypy <경로>

class RGB:
    def __init__(
        self, red: int, green: int, blue: int
    ) -> None:  # Changed
        self.red = red
        self.green = green
        self.blue = blue


obj = RGB(1, "bad", 3)   # 잘못된 타입
obj.red = "also bad"                   # 잘못된 타입
