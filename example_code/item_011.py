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

print("아이템 11")
print("Example 1")
a = 0b10111011
b = 0xC5F
print("이진수: %d, 십육진수: %d" % (a, b))


print("Example 2")
key = "my_var"
value = 1.234
formatted = "%-10s = %.2f" % (key, value)
print(formatted)


print("Example 3")
try:
    reordered_tuple = "%-10s = %.2f" % (value, key)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 4")
try:
    reordered_string = "%.2f = %-10s" % (key, value)
except:
    logging.exception('이 예외가 발생해야 함')
else:
    assert False


print("Example 5")
pantry = [
    ("아보카도", 1.25),
    ("바나나", 2.5),
    ("체리", 15),
]
for i, (item, count) in enumerate(pantry):
    print("#%d: %-10s = %.2f" % (i, item, count))


print("Example 6")
for i, (item, count) in enumerate(pantry):
    print(
        "#%d: %-10s = %d"
        % (
            i + 1,
            item.title(),
            round(count),
        )
    )


print("Example 7")
template = "%s는 음식을 좋아해. %s가 요리하는 모습을 봐요."
name = "철수"
formatted = template % (name, name)
print(formatted)


print("Example 8")
name = "brad"
formatted = template % (name.title(), name)
print(formatted)


print("Example 9")
key = "my_var"
value = 1.234

old_way = "%-10s = %.2f" % (key, value)

new_way = "%(key)-10s = %(value).2f" % {
    "key": key,  # 키를 처음에 넣음
    "value": value,
}

reordered = "%(key)-10s = %(value).2f" % {
    "value": value,
    "key": key,  # 키를 두번째에 넣음
}

assert old_way == new_way == reordered


print("Example 10")
name = "철수"

template = "%s는 음식을 좋아해. %s가 요리하는 모습을 봐요."
before = template % (name, name)   # 튜플

template = "%(name)s는 음식을 좋아해. %(name)s가 요리하는 모습을 봐요."
after = template % {"name": name}  # 딕셔너리

assert before == after


print("Example 11")
for i, (item, count) in enumerate(pantry):
    before = "#%d: %-10s = %d" % (
        i + 1,
        item.title(),
        round(count),
    )

    after = "#%(loop)d: %(item)-10s = %(count)d" % {
        "loop": i + 1,
        "item": item.title(),
        "count": round(count),
    }

    assert before == after


print("Example 12")
soup = "lentil"
formatted = "Today's soup is %(soup)s." % {"soup": soup}
print(formatted)


print("Example 13")
menu = {
    "soup": "lentil",
    "oyster": "tongyoung",
    "special": "schnitzel",
}
template = (
    "Today's soup is %(soup)s, "
    "buy one get two %(oyster)s oysters, "
    "and our special entrée is %(special)s."
)
formatted = template % menu
print(formatted)


print("Example 14")
a = 1234.5678
formatted = format(a, ",.2f")
print(formatted)

b = "my 문자열"
formatted = format(b, "^20s")
print("*", formatted, "*")


print("Example 15")
key = "my_var"
value = 1.234

formatted = "{} = {}".format(key, value)
print(formatted)


print("Example 16")
formatted = "{:<10} = {:.2f}".format(key, value)
print(formatted)


print("Example 17")
print("%.2f%%" % 12.5)
print("{} replaces {{}}".format(1.23))


print("Example 18")
formatted = "{1} = {0}".format(key, value)
print(formatted)


print("Example 19")
name = "돌쇠"
formatted = "{0}는 음식을 좋아해. {0}가 요리하는 모습을 봐요.".format(name)
print(formatted)


print("Example 20")
for i, (item, count) in enumerate(pantry):
    old_style = "#%d: %-10s = %d" % (
        i + 1,
        item.title(),
        round(count),
    )

    new_style = "#{}: {:<10s} = {}".format(
        i + 1,
        item.title(),
        round(count),
    )

    assert old_style == new_style


print("Example 21")
formatted = "첫번째 글자는 {menu[oyster][0]!r}".format(menu=menu)
print(formatted)


print("Example 22")
old_template = (
    "Today's soup is %(soup)s, "
    "buy one get two %(oyster)s oysters, "
    "and our special entrée is %(special)s."
)
old_formatted = old_template % {
    "soup": "lentil",
    "oyster": "tongyoung",
    "special": "schnitzel",
}

new_template = (
    "Today's soup is {soup}, "
    "buy one get two {oyster} oysters, "
    "and our special entrée is {special}."
)
new_formatted = new_template.format(
    soup="lentil",
    oyster="tongyoung",
    special="schnitzel",
)

assert old_formatted == new_formatted


print("Example 23")
key = "my_var"
value = 1.234

formatted = f"{key} = {value}"
print(formatted)


print("Example 24")
formatted = f"{key!r:<10} = {value:.2f}"
print(formatted)


print("Example 25")
f_string = f"{key:<10} = {value:.2f}"

c_tuple  = "%-10s = %.2f" % (key, value)

str_args = "{:<10} = {:.2f}".format(key, value)

str_kw   = "{key:<10} = {value:.2f}".format(key=key, value=value)

c_dict   = "%(key)-10s = %(value).2f" % {"key": key, "value": value}

assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string


print("Example 26")
for i, (item, count) in enumerate(pantry):
    old_style = "#%d: %-10s = %d" % (
        i + 1,
        item.title(),
        round(count),
    )

    new_style = "#{}: {:<10s} = {}".format(
        i + 1,
        item.title(),
        round(count),
    )

    f_string = f"#{i+1}: {item.title():<10s} = {round(count)}"

    assert old_style == new_style == f_string


print("Example 27")
for i, (item, count) in enumerate(pantry):
    print(f"#{i+1}: "
          f"{item.title():<10s} = "
          f"{round(count)}")


print("Example 28")
places = 3
number = 1.23456
print(f"내가 고른 숫자는 {number:.{places}f}")
