# Copyright 2024 Geoffrey R. Scheller
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

from __future__ import annotations

from typing import Optional, Final, Never
from grscheller.experimental.lazy import Lazy11, Lazy01

def add2_if_pos(x: int) -> int|Never:
    if x < 1:
        raise ValueError
    return x + 2

def evaluate_it(lz: Lazy11[int, int]) -> int:
    if lz.eval():
        return lz.result().get()
    else:
        return -1

class Test_Lazy11:
    def test_happy_path(self) -> None:
        assert evaluate_it(Lazy11(add2_if_pos, 5)) == 7

    def test_sad_path(self) -> None:
        assert evaluate_it(Lazy11(add2_if_pos, -42)) == -1


def hello() -> str|Never:
    hello = "helloooo"
    while len(hello) > 1:
        if hello == 'hello':
            return hello
        else:
            hello = hello[:-1]
    raise ValueError('hello')

def no_hello() -> str|Never:
    hello = "helloooo"
    while len(hello) > 1:
        if hello == 'hello':
            raise RuntimeError('failed as expected')
        else:
            hello = hello[:-1]
    return hello

def return_str(lz: Lazy01[str]) -> str:
    if lz.eval():
        return lz.result().get()
    else:
        esc = lz.exception().get()
        return f'Error: {esc}'

class Test_Lazy01:
    def test_happy_path(self) -> None:
        lz_good = Lazy01(hello, pure=False)
        assert return_str(lz_good) == 'hello'

    def test_sad_path(self) -> None:
        lz_bad = Lazy01(no_hello, pure=False)
        assert return_str(lz_bad) == 'Error: failed as expected'

