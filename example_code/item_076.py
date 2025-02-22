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
class EOFError(Exception):
    pass

class Connection:
    def __init__(self, connection):
        self.connection = connection
        self.file = connection.makefile("rb")

    def send(self, command):
        line = command + "\n"
        data = line.encode()
        self.connection.send(data)

    def receive(self):
        line = self.file.readline()
        if not line:
            raise EOFError("연결 닫힘")
        return line[:-1].decode()


print("Example 2")
import random

WARMER = "Warmer"
COLDER = "Colder"
SAME = "Same"
UNSURE = "Unsure"
CORRECT = "Correct"

class UnknownCommandError(Exception):
    pass

class ServerSession(Connection):
    def __init__(self, *args):
        super().__init__(*args)
        self.clear_state()


    print("Example 3")
    def loop(self):
        while command := self.receive():
            match command.split(" "):
                case "PARAMS", lower, upper:
                    self.set_params(lower, upper)
                case ["NUMBER"]:
                    self.send_number()
                case "REPORT", decision:
                    self.receive_report(decision)
                case ["CLEAR"]:
                    self.clear_state()
                case _:
                    raise UnknownCommandError(command)


    print("Example 4")
    def set_params(self, lower, upper):
        self.clear_state()
        self.lower = int(lower)
        self.upper = int(upper)


    print("Example 5")
    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    def send_number(self):
        guess = self.next_guess()
        self.guesses.append(guess)
        self.send(format(guess))


    print("Example 6")
    def receive_report(self, decision):
        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f"서버: {last}은 {decision}")


    print("Example 7")
    def clear_state(self):
        self.lower = None
        self.upper = None
        self.secret = None
        self.guesses = []


print("Example 8")
import contextlib
import time

@contextlib.contextmanager
def new_game(connection, lower, upper, secret):
    print(
        f"{lower}와 {upper} 사이의 수를 정합니다!"
        f" 조용, 비밀 번호는 {secret}입니다."
    )
    connection.send(f"PARAMS {lower} {upper}")
    try:
        yield ClientSession(
            connection.send,
            connection.receive,
            secret,
        )
    finally:
        # 출력이 여러분의 예상과 맞아 떨어지게 함
        time.sleep(0.1)
        connection.send("CLEAR")


print("Example 9")
import math

class ClientSession:
    def __init__(self, send, receive, secret):
        self.send = send
        self.receive = receive
        self.secret = secret
        self.last_distance = None


    print("Example 10")
    def request_number(self):
        self.send("NUMBER")
        data = self.receive()
        return int(data)


    print("Example 11")
    def report_outcome(self, number):
        new_distance = math.fabs(number - self.secret)

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            decision = UNSURE
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER
        else:
            decision = SAME

        self.last_distance = new_distance

        self.send(f"REPORT {decision}")
        return decision


    print("Example 12")
    def __iter__(self):
        while True:
            number = self.request_number()
            decision = self.report_outcome(number)
            yield number, decision
            if decision == CORRECT:
                return


print("Example 13")
import socket
from threading import Thread

def handle_connection(connection):
    with connection:
        session = ServerSession(connection)
        try:
            session.loop()
        except EOFError:
            pass

def run_server(address):
    with socket.socket() as listener:
        # 포트를 재사용하게 설정함
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(address)
        listener.listen()
        while True:
            connection, _ = listener.accept()
            thread = Thread(
                target=handle_connection,
                args=(connection,),
                daemon=True,
            )
            thread.start()


print("Example 14")
def run_client(address):
    with socket.create_connection(address) as server_sock:
        server = Connection(server_sock)

        with new_game(server, 1, 5, 3) as session:
            results = [outcome for outcome in session]

        with new_game(server, 10, 15, 12) as session:
            for outcome in session:
                results.append(outcome)

        with new_game(server, 1, 3, 2) as session:
            it = iter(session)
            while True:
                try:
                    outcome = next(it)
                except StopIteration:
                    break
                else:
                    results.append(outcome)

    return results


print("Example 15")
def main():
    address = ("127.0.0.1", 1234)
    server_thread = Thread(
        target=run_server, args=(address,), daemon=True
    )
    server_thread.start()

    results = run_client(address)
    for number, outcome in results:
        print(f"클라이언트: {number}은 {outcome}")

main()


print("Example 16")
class AsyncConnection:
    def __init__(self, reader, writer):      # 변경함
        self.reader = reader                 # 변경함
        self.writer = writer                 # 변경함

    async def send(self, command):
        line = command + "\n"
        data = line.encode()
        self.writer.write(data)              # 변경함
        await self.writer.drain()            # 변경함

    async def receive(self):
        line = await self.reader.readline()  # 변경함
        if not line:
            raise EOFError("연결 닫힘")
        return line[:-1].decode()


print("Example 17")
class AsyncServerSession(AsyncConnection):  # 변경함
    def __init__(self, *args):
        super().__init__(*args)
        self.clear_state()


    print("Example 18")
    async def loop(self):                       # 변경함
        while command := await self.receive():  # 변경함
            match command.split(" "):
                case "PARAMS", lower, upper:
                    self.set_params(lower, upper)
                case ["NUMBER"]:
                    await self.send_number()    # 변경함
                case "REPORT", decision:
                    self.receive_report(decision)
                case ["CLEAR"]:
                    self.clear_state()
                case _:
                    raise UnknownCommandError(command)


    print("Example 19")
    def set_params(self, lower, upper):
        self.clear_state()
        self.lower = int(lower)
        self.upper = int(upper)


    print("Example 20")
    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    async def send_number(self):                    # 변경함
        guess = self.next_guess()
        self.guesses.append(guess)
        await self.send(format(guess))              # 변경함


    print("Example 21")
    def receive_report(self, decision):
        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f"서버: {last}은 {decision}")

    def clear_state(self):
        self.lower = None
        self.upper = None
        self.secret = None
        self.guesses = []


print("Example 22")
@contextlib.asynccontextmanager                              # 변경함
async def new_async_game(connection, lower, upper, secret):  # 변경함
    print(
        f"{lower}와 {upper} 사이의 수를 정합니다!"
        f" 조용, 비밀 번호는 {secret} 입니다."
    )
    await connection.send(f"PARAMS {lower} {upper}")         # 변경함
    try:
        yield AsyncClientSession(
            connection.send,
            connection.receive,
            secret,
        )
    finally:
        # 출력이 스레드 버전과 똑같게 조정함
        await asyncio.sleep(0.1)
        await connection.send("CLEAR")                       # 변경함


print("Example 23")
class AsyncClientSession:
    def __init__(self, send, receive, secret):
        self.send = send
        self.receive = receive
        self.secret = secret
        self.last_distance = None


    print("Example 24")
    async def request_number(self):
        await self.send("NUMBER")    # Changed
        data = await self.receive()  # Changed
        return int(data)


    print("Example 25")
    async def report_outcome(self, number):    # Changed
        new_distance = math.fabs(number - self.secret)

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            decision = UNSURE
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER
        else:
            decision = SAME

        self.last_distance = new_distance

        await self.send(f"REPORT {decision}")  # 변경함
        return decision


    print("Example 26")
    async def __aiter__(self):                            # 변경함
        while True:
            number = await self.request_number()          # 변경함
            decision = await self.report_outcome(number)  # 변경함
            yield number, decision
            if decision == CORRECT:
                return


print("Example 27")
import asyncio

async def handle_async_connection(reader, writer):
    session = AsyncServerSession(reader, writer)
    try:
        await session.loop()
    except EOFError:
        pass

async def run_async_server(address):
    server = await asyncio.start_server(
        handle_async_connection, *address
    )
    async with server:
        await server.serve_forever()


print("Example 28")
async def run_async_client(address):
    # 연결을 시도하기 전에 서버를 기다린다
    await asyncio.sleep(0.1)

    streams = await asyncio.open_connection(*address)  # 새 기능
    client = AsyncConnection(*streams)                 # 새 기능

    async with new_async_game(client, 1, 5, 3) as session:
        results = [outcome async for outcome in session]

    async with new_async_game(client, 10, 15, 12) as session:
        async for outcome in session:
            results.append(outcome)

    async with new_async_game(client, 1, 3, 2) as session:
        it = aiter(session)
        while True:
            try:
                outcome = await anext(it)
            except StopAsyncIteration:
                break
            else:
                results.append(outcome)

    _, writer = streams                                # 새 기능
    writer.close()                                     # 새 기능
    await writer.wait_closed()                         # 새 기능

    return results


print("Example 29")
async def main_async():
    address = ("127.0.0.1", 4321)

    server = run_async_server(address)
    asyncio.create_task(server)

    results = await run_async_client(address)
    for number, outcome in results:
        print(f"클라이언트: {number}은 {outcome}")

logging.getLogger().setLevel(logging.ERROR)

asyncio.run(main_async())

logging.getLogger().setLevel(logging.DEBUG)
