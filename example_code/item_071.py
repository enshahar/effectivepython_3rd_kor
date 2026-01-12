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

print("아이템 71")
print("Example 1")
ALIVE = "*"
EMPTY = "-"


print("Example 2")
class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        output = ""
        for row in self.rows:
            for cell in row:
                output += cell
            output += "\n"
        return output


print("Example 3")
grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)
print(grid)


print("Example 4")
def count_neighbors(y, x, get_cell):
    n_ = get_cell(y - 1, x + 0) # 북(N)
    ne = get_cell(y - 1, x + 1) # 북동(NE)
    e_ = get_cell(y + 0, x + 1) # 동(E)
    se = get_cell(y + 1, x + 1) # 남동(SE)
    s_ = get_cell(y + 1, x + 0) # 남(S)
    sw = get_cell(y + 1, x - 1) # 남서(SW)
    w_ = get_cell(y + 0, x - 1) # 서(W)
    nw = get_cell(y - 1, x - 1) # 북서(NW)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


alive = {(9, 5), (9, 6)}
seen = set()

def fake_get(y, x):
    position = (y, x)
    seen.add(position)
    return ALIVE if position in alive else EMPTY

count = count_neighbors(10, 5, fake_get)
assert count == 2

expected_seen = {
    (9, 5),
    (9, 6),
    (10, 6),
    (11, 6),
    (11, 5),
    (11, 4),
    (10, 4),
    (9, 4),
}
assert seen == expected_seen


print("Example 5")
def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # 살아 있는 이웃이 너무 적음: 죽음
        elif neighbors > 3:
            return EMPTY     # 살아 있는 이웃이 너무 많음: 죽음
    else:
        if neighbors == 3:
            return ALIVE     # 죽은 셀에서 살아있는 셀로 변함
    return state

assert game_logic(ALIVE, 0) == EMPTY
assert game_logic(ALIVE, 1) == EMPTY
assert game_logic(ALIVE, 2) == ALIVE
assert game_logic(ALIVE, 3) == ALIVE
assert game_logic(ALIVE, 4) == EMPTY
assert game_logic(EMPTY, 0) == EMPTY
assert game_logic(EMPTY, 1) == EMPTY
assert game_logic(EMPTY, 2) == EMPTY
assert game_logic(EMPTY, 3) == ALIVE
assert game_logic(EMPTY, 4) == EMPTY


print("Example 6")
def step_cell(y, x, get_cell, set_cell):
    state = get_cell(y, x)
    neighbors = count_neighbors(y, x, get_cell)
    next_state = game_logic(state, neighbors)
    set_cell(y, x, next_state)


alive = {(10, 5), (9, 5), (9, 6)}
new_state = None

def fake_get(y, x):
    return ALIVE if (y, x) in alive else EMPTY

def fake_set(y, x, state):
    global new_state
    new_state = state

# Stay alive
step_cell(10, 5, fake_get, fake_set)
assert new_state == ALIVE

# Stay dead
alive.remove((10, 5))
step_cell(10, 5, fake_get, fake_set)
assert new_state == EMPTY

# Regenerate
alive.add((10, 6))
step_cell(10, 5, fake_get, fake_set)
assert new_state == ALIVE


print("Example 7")
def simulate(grid):
    next_grid = Grid(grid.height, grid.width)
    for y in range(grid.height):
        for x in range(grid.width):
            step_cell(y, x, grid.get, next_grid.set)
    return next_grid


print("Example 8")
class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.splitlines()) + 1)

        rows = [""] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = " " * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += " | "

        return "\n".join(rows)


columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate(grid)

print(columns)


print("Example 9")
def game_logic(state, neighbors):
    #  블러킹 I/O를 여기서 수행한다
    data = my_socket.recv(100)
