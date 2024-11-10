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

from typing import Optional, Final
from grscheller.experimental.lazy import Lazy

def add2_if_pos(x: int) -> int|Never:
    if x < 1:
        raise ValueError
    return x + 2

def evaluate_it(lz: Lazy[int, int]) -> int:
    if lz.eval():
        return lz()
    else:
        return -1

class Test_Lazy:
    def test_happy_path(self) -> None:
        assert evaluate_it(Lazy(add2_if_pos, 5)) == 7
    
    def test_sad_path(self) -> None:
        assert evaluate_it(Lazy(add2_if_pos, -42)) == -1 
