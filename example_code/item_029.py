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
class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


print("Example 2")
book = SimpleGradebook()
book.add_student("아이작 뉴튼")
book.report_grade("아이작 뉴튼", 90)
book.report_grade("아이작 뉴튼", 95)
book.report_grade("아이작 뉴튼", 85)

print(book.average_grade("아이작 뉴튼"))


print("Example 3")
from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        self._grades = {}                       # 외부 dict

    def add_student(self, name):
        self._grades[name] = defaultdict(list)  # 내부 dict

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count


print("Example 4")
book = BySubjectGradebook()
book.add_student("알버트 아인슈타인")
book.report_grade("알버트 아인슈타인", "수학", 75)
book.report_grade("알버트 아인슈타인", "수학", 65)
book.report_grade("알버트 아인슈타인", "체육", 90)
book.report_grade("알버트 아인슈타인", "체육", 95)
print(book.average_grade("알버트 아인슈타인"))


print("Example 5")
class WeightedGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))    # 변경함

    def average_grade(self, name):
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0
        for scores in by_subject.values():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:      # Added inner loop
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count


print("Example 6")
book = WeightedGradebook()
book.add_student("알버트 아인슈타인")
book.report_grade("알버트 아인슈타인", "수학", 75, 0.05)
book.report_grade("알버트 아인슈타인", "수학", 65, 0.15)
book.report_grade("알버트 아인슈타인", "수학", 70, 0.80)
book.report_grade("알버트 아인슈타인", "체육", 100, 0.40)
book.report_grade("알버트 아인슈타인", "체육", 85, 0.60)
print(book.average_grade("알버트 아인슈타인"))


print("Example 7")
grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight
print(average_grade)


print("Example 8")
grades = []
grades.append((95, 0.45, "참 잘했어요"))
grades.append((85, 0.55, "다음엔 더 잘할 수 있어요"))
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight
print(average_grade)


print("Example 9")
from dataclasses import dataclass

@dataclass(frozen=True)
class Grade:
    score: int
    weight: float


print("Example 10")
class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


print("Example 11")
class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


print("Example 12")
class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]


print("Example 13")
book = Gradebook()
albert = book.get_student("알버트 아인슈타인")
math = albert.get_subject("수학")
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject("체육")
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
