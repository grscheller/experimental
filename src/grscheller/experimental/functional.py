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

__all__ = [ 'swap', 'entup', 'detup', 'partial' ]

## Functional Utilities

def swap[U,V,R](f: Callable[[U,V],R]) -> Callable[[V,U],R]:
    """Swap arguments of a two argument function."""
    return (lambda v,u: f(u,v))

## Tupleizing Tools

def entup[**P, R](f: Callable[[P],R]) -> Callable[[tuple[P]], R]:
    def F(args: tuple[P]) -> R:
        return f(*args)
    return F

# TODO: Think I will need to use something called a ParamSpec from
# 
#   typing.ParamSpec(name, *, bound=None, covariant=False, contravariant=False)
#
# It is part of something called "structured typing".
#
# To create a ParamSpec in pre-3.12 Python one would use
# 
#   type IntFunc[**P] = Callable[P, int]
#
# Consider these examples from the Python 3.12 documentation

from threading import Lock
from typing import Concatenate

# Use this lock to ensure that only one thread is executing a function
# at any time.
my_lock = Lock()

def with_lock[**P, R](f: Callable[Concatenate[Lock, P], R]) -> Callable[P, R]:
    '''A type-safe decorator which provides a lock.'''
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        # Provide the lock as the first argument.
        return f(my_lock, *args, **kwargs)
    return inner

@with_lock
def sum_threadsafe(lock: Lock, numbers: list[float]) -> float:
    '''Add a list of numbers together in a thread-safe manner.'''
    with lock:
        return sum(numbers)

reveal_type(sum_threadsafe)

# We don't need to pass in the lock ourselves thanks to the decorator.
sum_threadsafe([1.1, 2.2, 3.3])

# Another example,

import logging

def add_logging[T, **P](f: Callable[P, T]) -> Callable[P, T]:
    '''A type-safe decorator to add logging to a function.'''
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        logging.info(f'{f.__name__} was called')
        return f(*args, **kwargs)
    return inner

@add_logging
def add_two(x: float, y: float) -> float:
    '''Add two numbers together.'''
    return x + y

# Note that:
#
#  1, The type checker can’t type check the inner function
#     because *args and **kwargs have to be typed Any.
#
#  2. cast() may be required in the body of the add_logging decorator
#     when returning the inner function, or the static type checker
#     must be told to ignore the return inner. *
# 
#  * reveal_type() seems to work with these examples????

def add(x: float, y:float) -> float:
    return x+y

add_with_logging = add_logging(add)
reveal_type(add_with_logging)

# Any case, instead of just passing the ParamSpec, maybe I can repackage it?

