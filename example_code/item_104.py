#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2024 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.00
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

print("아이템 104")
print("Example 1")
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


print("Example 2")
def add_book(queue, book):
    queue.append(book)
    queue.sort(key=lambda x: x.due_date, reverse=True)

queue = []
add_book(queue, Book("돈키호테", "2025-06-07"))
add_book(queue, Book("프랑켄슈타인", "2025-06-05"))
add_book(queue, Book("레미제라블", "2025-06-08"))
add_book(queue, Book("전쟁과 평화", "2025-06-03"))


print("Example 3")
class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book

    raise NoOverdueBooks


print("Example 4")
now = "2025-06-10"

found = next_overdue_book(queue, now)
print(found.due_date, found.title)

found = next_overdue_book(queue, now)
print(found.due_date, found.title)


print("Example 5")
def return_book(queue, book):
    queue.remove(book)

queue = []
book = Book("보물섬", "2025-06-04")

add_book(queue, book)
print("반납 전:", [x.title for x in queue])

return_book(queue, book)
print("반납 후: ", [x.title for x in queue])


print("Example 6")
try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # 이 문장이 실행되리라 예상함
else:
    assert False  # 이 문장은 결코 실행되지 않음


print("Example 7")
import random
import timeit

def list_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            queue.append(i)
            queue.sort(reverse=True)

        while queue:
            queue.pop()

    return timeit.timeit(
        setup="queue, to_add = prepare()",
        stmt=f"run(queue, to_add)",
        globals=locals(),
        number=1,
    )


print("Example 8")
for i in range(1, 6):
    count = i * 1_000
    delay = list_overdue_benchmark(count)
    print(f"개수 {count:>5,} 시간: {delay*1e3:>6.2f}밀리초")


print("Example 9")
def list_return_benchmark(count):
    def prepare():
        queue = list(range(count))
        random.shuffle(queue)

        to_return = list(range(count))
        random.shuffle(to_return)

        return queue, to_return

    def run(queue, to_return):
        for i in to_return:
            queue.remove(i)

    return timeit.timeit(
        setup="queue, to_return = prepare()",
        stmt=f"run(queue, to_return)",
        globals=locals(),
        number=1,
    )


print("Example 10")
for i in range(1, 6):
    count = i * 1_000
    delay = list_return_benchmark(count)
    print(f"개수 {count:>5,} 시간: {delay*1e3:>6.2f}밀리초")


print("Example 11")
from heapq import heappush

def add_book(queue, book):
    heappush(queue, book)


print("Example 12")
try:
    queue = []
    add_book(queue, Book("작은 아씨들", "2025-06-05"))
    add_book(queue, Book("타임 머신", "2025-05-30"))
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 13")
import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date


print("Example 14")
queue = []
add_book(queue, Book("오만과 편견", "2025-06-01"))
add_book(queue, Book("타임 머신", "2025-05-30"))
add_book(queue, Book("죄와 벌", "2025-06-06"))
add_book(queue, Book("폭풍의 언덕", "2025-06-12"))
print([b.title for b in queue])


print("Example 15")
queue = [
    Book("오만과 편견", "2025-06-01"),
    Book("타임 머신", "2025-05-30"),
    Book("죄와 벌", "2025-06-06"),
    Book("폭풍의 언덕", "2025-06-12"),
]
queue.sort()
print([b.title for b in queue])


print("Example 16")
from heapq import heapify

queue = [
    Book("오만과 편견", "2025-06-01"),
    Book("타임 머신", "2025-05-30"),
    Book("죄와 벌", "2025-06-06"),
    Book("폭풍의 언덕", "2025-06-12"),
]
heapify(queue)
print([b.title for b in queue])


print("Example 17")
from heapq import heappop

def next_overdue_book(queue, now):
    if queue:
        book = queue[0]     # 만기가 가장 이른 책이 맨 앞에 있다
        if book.due_date < now:
            heappop(queue)  # 연체된 책을 제거한다
            return book

    raise NoOverdueBooks


print("Example 18")
now = "2025-06-02"

book = next_overdue_book(queue, now)
print(book.due_date, book.title)

book = next_overdue_book(queue, now)
print(book.due_date, book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass  # 이 문장이 실행되리라 예상함
else:
    assert False  # 이 문장은 결코 실행되지 않음


print("Example 19")
def heap_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            heappush(queue, i)
        while queue:
            heappop(queue)

    return timeit.timeit(
        setup="queue, to_add = prepare()",
        stmt=f"run(queue, to_add)",
        globals=locals(),
        number=1,
    )


print("Example 20")
for i in range(1, 6):
    count = i * 10_000
    delay = heap_overdue_benchmark(count)
    print(f"개수 {count:>5,} 시간: {delay*1e3:>6.2f}밀리초")


print("Example 21")
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False  # 새로운 필드

    def __lt__(self, other):
        return self.due_date < other.due_date


print("Example 22")
def next_overdue_book(queue, now):
    while queue:
        book = queue[0]
        if book.returned:
            heappop(queue)
            continue

        if book.due_date < now:
            heappop(queue)
            return book

        break

    raise NoOverdueBooks


queue = []

book = Book("오만과 편견", "2025-06-01")
add_book(queue, book)

book = Book("타임 머신", "2025-05-30")
add_book(queue, book)
book.returned = True

book = Book("죄와 벌", "2025-06-06")
add_book(queue, book)
book.returned = True

book = Book("폭풍의 언덕", "2025-06-12")
add_book(queue, book)

now = "2025-06-11"

book = next_overdue_book(queue, now)
assert book.title == "오만과 편견"

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass  # Expected
else:
    assert False  # Doesn't happen


print("Example 23")
def return_book(queue, book):
    book.returned = True


assert not book.returned
return_book(queue, book)
assert book.returned
