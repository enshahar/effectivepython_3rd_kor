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

print("아이템 58")
print("Example 1")
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


print("Example 2")
r0 = OldResistor(50e3)
print("이전:", r0.get_ohms())
r0.set_ohms(10e3)
print("이후:", r0.get_ohms())


print("Example 3")
r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3


print("Example 4")
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3
print(
    f"{r1.ohms} 옴, " f"{r1.voltage} 볼트, " f"{r1.current} 암페어"
)


print("Example 5")
r1.ohms += 5e3


print("Example 6")
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


print("Example 7")
r2 = VoltageResistance(1e2)
print(f"이전: {r2.current:.2f} 암페어")
r2.voltage = 10
print(f"이후: {r2.current:.2f} 암페어")


print("Example 8")
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f"저항은 > 0여야 함; 현재 값은 {ohms}")
        self._ohms = ohms


print("Example 9")
try:
    r3 = BoundedResistance(1e3)
    r3.ohms = 0
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 10")
try:
    BoundedResistance(-5)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 11")
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, "_ohms"):
            raise AttributeError("저항은 불변임")
        self._ohms = ohms


print("Example 12")
try:
    r4 = FixedResistance(1e3)
    r4.ohms = 2e3
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 13")
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms


print("Example 14")
r7 = MysteriousResistor(10)
r7.current = 0.1
print(f"이전: {r7.voltage:.2f}")
r7.ohms
print(f"이후: {r7.voltage:.2f}")
