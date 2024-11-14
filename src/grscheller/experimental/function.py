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

"""### Module fp.functional - FP tools function composition

Library to compose and partially apply functions.

* not a replacement for the std library functools
  * functools is more about decorating functions
  * fp.functional are tools which treat functions as first class objects

#### Functional utilities:

* **function swap:** swap the arguments of a 2 argument function

---

#### Tupleizing and detupleizing functions (TODO)

* **function entup:** convert function to one taking a tuple of original arguments
* **function detup:** reverse above procedure

---

#### Partially apply function arguments

* **function partial:** returns a partially applied function

---

"""
from __future__ import annotations
from typing import Callable, cast, Iterator, Iterable, overload

__all__ = [ 'swap', 'entuple' ]

## Functional Utilities

def swap[U,V,R](f: Callable[[U,V],R]) -> Callable[[V,U],R]:
    """Swap arguments of a two argument function."""
    return (lambda v,u: f(u,v))

## Tupleizing Tools

def entuple[**P, R](f: Callable[P, R]) -> Callable[[tuple[P.args]], R]:
    def F(arguments: tuple[*P.args]) -> R:
        return f(*arguments)
    return F

