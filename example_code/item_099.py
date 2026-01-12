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

print("아이템 100")
print("Example 1")
def timecode_to_index(video_id, timecode):
    return 1234
    # 비디오 데이터의 바이트 오프셋을 반환한다

def request_chunk(video_id, byte_offset, size):
    pass
    # video_id에 대한 비디오 데이터 중에 바이트 오프셋부터 size만큼을 반환한다

video_id = ...
timecode = "01:09:14:28"
byte_offset = timecode_to_index(video_id, timecode)
size = 20 * 1024 * 1024
video_data = request_chunk(video_id, byte_offset, size)


print("Example 2")
class NullSocket:
    def __init__(self):
        self.handle = open(os.devnull, "wb")

    def send(self, data):
        self.handle.write(data)

socket = ...            # 클라이언트가 연결한 소켓
video_data = ...        # video_id에 해당하는 데이터가 들어 있는 bytes
byte_offset = ...       # 요청받은 시작 위치
size = 20 * 1024 * 1024 # 요청받은 데이터 크기
import os

socket = NullSocket()
video_data = 100 * os.urandom(1024 * 1024)
byte_offset = 1234

chunk = video_data[byte_offset : byte_offset + size]
socket.send(chunk)


print("Example 3")
import timeit

def run_test():
    chunk = video_data[byte_offset : byte_offset + size]
    # socket.send(chunk)를 호출해야 하지만 벤치마크를 위해 무시한다

result = (
    timeit.timeit(
        stmt="run_test()",
        globals=globals(),
        number=100,
    )
    / 100
)

print(f"{result:0.9f} 초")


print("Example 4")
data = b"shave and a haircut, two bits"
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print("크기:       ", chunk.nbytes)
print("뷰데이터:   ", chunk.tobytes())
print("기저 데이터:", chunk.obj)


print("Example 5")
video_view = memoryview(video_data)

def run_test():
    chunk = video_view[byte_offset : byte_offset + size]
    # socket.send(chunk)를 호출해야 하지만 벤치마크를 위해 무시한다

result = (
    timeit.timeit(
        stmt="run_test()",
        globals=globals(),
        number=100,
    )
    / 100
)

print(f"{result:0.9f} 초")


print("Example 6")
class FakeSocket:

    def recv(self, size):
        return video_view[byte_offset : byte_offset + size]

    def recv_into(self, buffer):
        source_data = video_view[byte_offset : byte_offset + size]
        buffer[:] = source_data

socket = ...       # 클라이언트가 연결한 소켓
video_cache = ...  # 서버로 들어오는 비디오 스트림의 캐시
byte_offset = ...  # 데이터 버퍼 위치
size = 1024 * 1024 # 데이터 덩어리 크기
socket = FakeSocket()
video_cache = video_data[:]
byte_offset = 1234

chunk = socket.recv(size)
video_view = memoryview(video_cache)
before = video_view[:byte_offset]
after = video_view[byte_offset + size :]
new_cache = b"".join([before, chunk, after])


print("Example 7")
def run_test():
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size :]
    new_cache = b"".join([before, chunk, after])

result = (
    timeit.timeit(
        stmt="run_test()",
        globals=globals(),
        number=100,
    )
    / 100
)

print(f"{result:0.9f} 초")


print("Example 8")
try:
    my_bytes = b"hello"
    my_bytes[0] = 0x79
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 9")
my_array = bytearray(b"hello")
my_array[0] = 0x79
print(my_array)


print("Example 10")
my_array = bytearray(b"row, row, row your boat")
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b"-10 bytes-"
print(my_array)


print("Example 11")
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset : byte_offset + size]
socket.recv_into(chunk)


print("Example 12")
def run_test():
    chunk = write_view[byte_offset : byte_offset + size]
    socket.recv_into(chunk)

result = (
    timeit.timeit(
        stmt="run_test()",
        globals=globals(),
        number=100,
    )
    / 100
)

print(f"{result:0.9f} 초")
