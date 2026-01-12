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

print("아이템 57")
print("Example 1")
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts


print("Example 2")
foo = FrequencyList(["a", "b", "a", "c", "b", "a", "d"])
print("길이:      ", len(foo))
foo.pop()  # 맨 끝의 "d" 삭제
print("pop한 다음:", repr(foo))
print("빈도:      ", foo.frequency())


print("Example 3")
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


print("Example 4")
bar = [1, 2, 3]
bar[0]


print("Example 5")
bar.__getitem__(0)


print("Example 6")
class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f"Index {index} is out of range")


print("Example 7")
tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(6, right=IndexableNode(7)),
    ),
    right=IndexableNode(15, left=IndexableNode(11)),
)


print("Example 8")
print("왼쪽.오른쪽.오른쪽:", tree.left.right.right.value)
print("인덱스 0:          ", tree[0])
print("인덱스 1:          ", tree[1])
print("11이 트리에 있나?  ", 11 in tree)
print("17이 트리에 있나?  ", 17 in tree)
print("트리: ", list(tree))

try:
    tree[100]
except IndexError:
    pass
else:
    assert False


print("Example 9")
try:
    len(tree)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 10")
class SequenceNode(IndexableNode):
    def __len__(self):
        count = 0
        for _ in self._traverse():
            count += 1
        return count


print("Example 11")
tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(6, right=SequenceNode(7)),
    ),
    right=SequenceNode(15, left=SequenceNode(11)),
)

print("트리 길이는", len(tree))


print("Example 12")
try:
    # Make sure that this doesn't work
    tree.count(4)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 13")
try:
    from collections.abc import Sequence
    
    class BadType(Sequence):
        pass
    
    foo = BadType()
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 14")
class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(6, right=BetterNode(7)),
    ),
    right=BetterNode(15, left=BetterNode(11)),
)

print("7의 인덱스는", tree.index(7))
print("10이 등장한 횟수는", tree.count(10))
