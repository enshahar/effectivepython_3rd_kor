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

print("아이템 70")
print("Example 1")
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item


print("Example 2")
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()


    print("Example 3")
    def put(self, item):
        with self.lock:
            self.items.append(item)


    print("Example 4")
    def get(self):
        with self.lock:
            return self.items.popleft()


print("Example 5")
from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0


    print("Example 6")
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)  # 처리할 작업이 없음
            except AttributeError:
                # 예제 코드에서 쉽게 종료를 시키기 위한 장치.
                # 하지만 실전에서는 오류 원인에 따라 적절한 처리를 해야 함.
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


print("Example 7")
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]


print("Example 8")
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())


print("Example 9")
while len(done_queue.items) < 1000:
    # 기다리는 동안 다른 유용한 작업을 수행한다
    time.sleep(0.1)
# run 메서드에서 예외를 발생시켜서 모든 스레드를 종료시킨다
for thread in threads:
    thread.in_queue = None
    thread.join()


print("Example 10")
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f"아이템을 {processed} 개 처리하는 동안 " f" 폴링을 {polled} 번 수행함")


print("Example 11")
from queue import Queue

my_queue = Queue()

def consumer():
    print("소비자 대기중")
    my_queue.get()            # 다음에 보여줄 put()이 실행된 다음에 시행된다
    print("소비자 끝남")

thread = Thread(target=consumer)
thread.start()


print("생산자 put 실행")
my_queue.put(object())     # 앞에서 본 get()이 실행되기 전에 실행된다.
print("생산자 끝남")
thread.join()


print("Example 13")
my_queue = Queue(1)  # 버퍼 크기 1

def consumer():
    time.sleep(0.1)  # 대기
    my_queue.get()   # 두번째로 실행됨
    print("소비자 얻음 1")
    my_queue.get()   # 네번째로 실행됨
    print("소비자 얻음 2")
    print("소비자 끝남")

thread = Thread(target=consumer)
thread.start()


print("Example 14")
my_queue.put(object())  # 첫번째로 실행됨
print("생산자 put 1")
my_queue.put(object()) # 세번째로 실행됨
print("생산자 put 2")
print("생산자 끝남")
thread.join()


print("Example 15")
in_queue = Queue()

def consumer():
    print("소비자 대기중")
    work = in_queue.get()  # 두 번째로 실행됨
    print("소비자 작업중")
    # 작업을 수행한다
    print("소비자 끝남")
    in_queue.task_done()  # 세 번째로 실행됨

thread = Thread(target=consumer)
thread.start()


print("Example 16")
print("생산자 put 하는 중")
in_queue.put(object())    # 첫 번째로 실행됨
print("생산자 대기중")
in_queue.join()           # 네 번째로 실행됨
print("생산자 끝남")
thread.join()


print("Example 17")
from queue import ShutDown

my_queue2 = Queue()

def consumer():
    while True:
        try:
            item = my_queue2.get()
        except ShutDown:
            print("끝내는 중!")
            return
        else:
            print("아이템 얻음", item)
            my_queue2.task_done()

thread = Thread(target=consumer)
my_queue2.put(1)
my_queue2.put(2)
my_queue2.put(3)
my_queue2.shutdown()

thread.start()

my_queue2.join()
thread.join()
print("끝남")


print("Example 18")
class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            try:
                item = self.in_queue.get()
            except ShutDown:
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.in_queue.task_done()


print("Example 19")
download_queue = Queue()
resize_queue = Queue(100)
upload_queue = Queue(100)
done_queue = Queue()

threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()


print("Example 20")
for _ in range(1000):
    download_queue.put(object())


print("Example 21")
download_queue.shutdown()
download_queue.join()

resize_queue.shutdown()
resize_queue.join()

upload_queue.shutdown()
upload_queue.join()


print("Example 22")
done_queue.shutdown()

counter = 0

while True:
    try:
        item = done_queue.get()
    except ShutDown:
        break
    else:
        # 원소를 처리한다
        done_queue.task_done()
        counter += 1

done_queue.join()

for thread in threads:
    thread.join()

print(counter, "개의 아이템 끝남")


print("Example 23")
def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def drain_queue(input_queue):
    input_queue.shutdown()

    counter = 0

    while True:
        try:
            item = input_queue.get()
        except ShutDown:
            break
        else:
            input_queue.task_done()
            counter += 1

    input_queue.join()

    return counter


print("Example 24")
download_queue = Queue()
resize_queue = Queue(100)
upload_queue = Queue(100)
done_queue = Queue()

threads = (
    start_threads(3, download, download_queue, resize_queue)
    + start_threads(4, resize, resize_queue, upload_queue)
    + start_threads(5, upload, upload_queue, done_queue)
)


print("Example 25")
for _ in range(2000):
    download_queue.put(object())

download_queue.shutdown()
download_queue.join()

resize_queue.shutdown()
resize_queue.join()

upload_queue.shutdown()
upload_queue.join()

counter = drain_queue(done_queue)

for thread in threads:
    thread.join()

print(counter, "개의 아이템 끝남")
