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
import subprocess

# 윈도우즈에서는 다음 두 줄의 주석을 제거해서 활성화해야 한다
# import os
# os.environ['COMSPEC'] = 'powershell'
result = subprocess.run(
    ["echo", "자식 프로세스로부터 안녕!"],
    capture_output=True,
    # 윈도우즈에서는 다음 줄을 활성화해야 한다
    # shell=True,
    encoding="utf-8",
)

result.check_returncode()  # 예외가 발생하지 않으면 문제 없이 잘 종료한 것이다
print(result.stdout)


print("Example 2")
# 윈도우즈에서는 원래 예제 코드가 아니라 다음 줄을 사용해야 한다
# proc = subprocess.Popen(['sleep', '1'], shell=True)
proc = subprocess.Popen(["sleep", "1"])
while proc.poll() is None:
    print("작업중...")
    # 시간이 걸리는 작업을 여기서 수행한다
    import time

    time.sleep(0.3)

print("종료 상태", proc.poll())


print("Example 3")
import time

start = time.perf_counter()
sleep_procs = []
for _ in range(10):
    # 윈도우즈에서는 원래 예제 코드가 아니라 다음 줄을 사용해야 한다
    # proc = subprocess.Popen(['sleep', '1'], shell=True)
    proc = subprocess.Popen(["sleep", "1"])
    sleep_procs.append(proc)


print("Example 4")
for proc in sleep_procs:
    proc.communicate()

end = time.perf_counter()
delta = end - start
print(f"{delta:.3} 초 걸림")


print("Example 5")
import os

# 윈도우에서는 OpenSSL을 설치한 다음에,
# 파워셀(파이썬 인터프리터가 아님)에서 다음과 같은 명령을 실행해 경로를 지정해야 할 수도 있다:
# $env:path = $env:path + ";C:\Program Files\OpenSSL-Win64\bin"

def run_encrypt(data):
    env = os.environ.copy()
    env["password"] = "zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1"
    proc = subprocess.Popen(
        ["openssl", "enc", "-des3", "-pbkdf2", "-pass", "env:password"],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    proc.stdin.write(data)
    proc.stdin.flush()  # 자식이 입력을 받도록 보장한다
    return proc


print("Example 6")
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)


print("Example 7")
for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])


print("Example 8")
def run_hash(input_stdin):
    return subprocess.Popen(
        ["openssl", "dgst", "-sha256", "-binary"],
        stdin=input_stdin,
        stdout=subprocess.PIPE,
    )


print("Example 9")
encrypt_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(100)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # 자식이 입력 스트림에 들어오는 데이터를 소비하고 communicate() 메서드가
    # 불필요하게 자식으로부터 오는 입력을 훔쳐가지 못하게 만든다.
    # 또 다운스트림 프로세스가 죽으면 SIGPIPE를 업스트림 프로세스에 전달한다.
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None


print("Example 10")
for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])
    assert proc.returncode == 0


print("Example 11")
# 윈도우즈에서는 원래 예제 코드가 아니라 다음 줄을 사용해야 한다
# proc = subprocess.Popen(['sleep', '10'], shell=True)
proc = subprocess.Popen(["sleep", "10"])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print("종료 상태", proc.poll())
