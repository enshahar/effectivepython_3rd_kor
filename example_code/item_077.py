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
class NoNewData(Exception):
    pass

def readline(handle):
    offset = handle.tell()
    handle.seek(0, 2)
    length = handle.tell()

    if length == offset:
        raise NoNewData

    handle.seek(offset, 0)
    return handle.readline()


print("Example 2")
import time

def tail_file(handle, interval, write_func):
    while not handle.closed:
        try:
            line = readline(handle)
        except NoNewData:
            time.sleep(interval)
        else:
            write_func(line)


print("Example 3")
from threading import Lock, Thread

def run_threads(handles, interval, output_path):
    with open(output_path, "wb") as output:
        lock = Lock()

        def write(data):
            with lock:
                output.write(data)

        threads = []
        for handle in handles:
            args = (handle, interval, write)
            thread = Thread(target=tail_file, args=args)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


print("Example 4")
# 핸들에 쓰는 라이터를 시뮬레이션하는 전체 코드
import collections
import os
import random
import string
from tempfile import TemporaryDirectory

def write_random_data(path, write_count, interval):
    with open(path, "wb") as f:
        for i in range(write_count):
            time.sleep(random.random() * interval)
            letters = random.choices(string.ascii_lowercase, k=10)
            data = f'{path}-{i:02}-{"".join(letters)}\n'
            f.write(data.encode())
            f.flush()

def start_write_threads(directory, file_count):
    paths = []
    for i in range(file_count):
        path = os.path.join(directory, str(i))
        with open(path, "w"):
            # 읽기 스레드를 폴링할 때 파일이 경로상에 존재하게 함
            pass
        paths.append(path)
        args = (path, 10, 0.1)
        thread = Thread(target=write_random_data, args=args)
        thread.start()
    return paths

def close_all(handles):
    time.sleep(1)
    for handle in handles:
        handle.close()

def setup():
    tmpdir = TemporaryDirectory()
    input_paths = start_write_threads(tmpdir.name, 5)

    handles = []
    for path in input_paths:
        handle = open(path, "rb")
        handles.append(handle)

    Thread(target=close_all, args=(handles,)).start()

    output_path = os.path.join(tmpdir.name, "merged")
    return tmpdir, input_paths, handles, output_path


print("Example 5")
def confirm_merge(input_paths, output_path):
    found = collections.defaultdict(list)
    with open(output_path, "rb") as f:
        for line in f:
            for path in input_paths:
                if line.find(path.encode()) == 0:
                    found[path].append(line)

    expected = collections.defaultdict(list)
    for path in input_paths:
        with open(path, "rb") as f:
            expected[path].extend(f.readlines())

    for key, expected_lines in expected.items():
        found_lines = found[key]
        assert (
            expected_lines == found_lines
        ), f"{expected_lines!r} == {found_lines!r}"

input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


print("Example 6")
import asyncio

# TODO: 더이상 아래 조치가 필요하지 않은지 검증해봐야 함
#
# 윈도우에서 ProactorEventLoop를 스레드 내부에서 생성할 수 없다.
# 시그널 핸들러를 등록하려고 하기 때문이다.
# 다음은 SelectorEventLoop 정책을 사용하는 대안이다.
# 참조: https://bugs.python.org/issue33792
# policy = asyncio.get_event_loop_policy()
# policy._loop_factory = asyncio.SelectorEventLoop
async def run_tasks_mixed(handles, interval, output_path):
    loop = asyncio.get_event_loop()

    output = await loop.run_in_executor(None, open, output_path, "wb")
    try:

        async def write_async(data):
            await loop.run_in_executor(None, output.write, data)

        def write(data):
            coro = write_async(data)
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            future.result()

        tasks = []
        for handle in handles:
            task = loop.run_in_executor(
                None, tail_file, handle, interval, write
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
    finally:
        await loop.run_in_executor(None, output.close)


print("Example 7")
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks_mixed(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


print("Example 8")
async def tail_async(handle, interval, write_func):
    loop = asyncio.get_event_loop()

    while not handle.closed:
        try:
            line = await loop.run_in_executor(None, readline, handle)
        except NoNewData:
            await asyncio.sleep(interval)
        else:
            await write_func(line)


print("Example 9")
async def run_tasks(handles, interval, output_path):
    loop = asyncio.get_event_loop()

    output = await loop.run_in_executor(None, open, output_path, "wb")
    try:

        async def write_async(data):
            await loop.run_in_executor(None, output.write, data)

        async with asyncio.TaskGroup() as group:
            for handle in handles:
                group.create_task(
                    tail_async(handle, interval, write_async)
                )
    finally:
        await loop.run_in_executor(None, output.close)


print("Example 10")
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

asyncio.run(run_tasks(handles, 0.1, output_path))

confirm_merge(input_paths, output_path)

tmpdir.cleanup()


print("Example 11")
def tail_file(handle, interval, write_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def write_async(data):
        await loop.run_in_executor(None, write_func, data)

    coro = tail_async(handle, interval, write_async)
    loop.run_until_complete(coro)


print("Example 12")
input_paths = ...
handles = ...
output_path = ...

tmpdir, input_paths, handles, output_path = setup()

run_threads(handles, 0.1, output_path)

confirm_merge(input_paths, output_path)

tmpdir.cleanup()
