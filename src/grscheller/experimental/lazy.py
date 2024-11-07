# Copyright 2023-2024 Geoffrey R. Scheller
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

"""### Module experimental.lazy - lazy function evaluations

Delayed function evaluations, if needed, usually in some inner scope. FP tools
for "non-strict" function evaluations.

#### Non-strict tooling:

* **class Lazy:** Delay function evaluation

"""
from __future__ import annotations

__all__ = [ 'Lazy' ]

from typing import Callable, Iterator
from grscheller.fp.err_handling import MB, XOR

class Lazy[D, R]():
    """Delayed function evaluation.

    Class instance delays the executable of a function where `Lazy(f, args)`
    constructs an object that can evaluate the Callable `f` with its arguments
    at a later time. The arguments to `f` are stored in the tuple `args`.

    * first argument `f` takes a function of a variable number of arguments
    * second argument `args` is the tuple of the arguments to be passed to `f`
      * where the type `~D` is the `tuple` type of the argument types to `f`
    * function is evaluated when the eval method is called
      * self._results set to `XOR[~R, MB[Exception]]`
      * where `~R` is the `tuple` type of the return types of `f`
    * result is cached unless `pure` is set to `False` in `__init__` method
    * class is callable with no arguments
      * if needed, will first evaluate `f` with its arguments
      * then, if successful, return a tuple of the resulting return values
      * otherwise, raise a RunTimeError
        * guard against this by
          * first calling the eval method
          * and then evaluating the Lazy object itself in a Boolean context
    * retrieve evaluated return values via
      * Lazy object's `__call__` method
      * Lazy object's `__iter__` method

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances.
    """
    __slots__ = '_f', '_args', '_results', '_pure'
    __match_args__ = '_args', '_results'

    def __init__(self, f: Callable[..., tuple[R]], args: D, pure: bool=True) -> None:
        self._f = f
        self._args = args
        self._pure = pure
        self._results: XOR[tuple[R, ...], MB[Exception]] = XOR(MB(), MB())

    def __bool__(self) -> bool:
        return True if self._results else False

    def is_evaluated(self) -> bool:
        return self._results != XOR(MB(), MB())

    def is_exceptional(self) -> bool:
        if self.is_evaluated():
            return False if self._results else True
        else:
            return False

    def eval(self) -> None:
        """Evaluate function with its arguments.

        * evaluate function
        * cache results or exceptions

        """
        if not (self._results and self._pure):
            try:
                result = self._f(*self._args)       # TODO: Need more functional tools to get around this limitation.
            except Exception as exc:                #       Change f to F where F is the "tuple-ized" version of f.
                self._results = XOR(MB(), MB(exc))
            else:
                if isinstance(result, tuple):
                    self._results = XOR(result, MB())
                elif result is None:
                    self._results = XOR((), MB())
                else:
                    self._results = XOR((result,), MB())

    def __iter__(self) -> Iterator[R]:
        if not self._results:
            self.eval()
        if self._results:
            for r in self._results.getLeft():
                yield r

    def __call__(self) -> tuple[R, ...]:
        self.eval()
        if self._results:
            return self._results.getLeft()
        else:
            msg = f"lazy: Lazy evaluated function raised exceptions"
            raise RuntimeError(msg)

### TODO
#   Write tests for what I got so far
#   1. before code gets too complicated
#   2. to help refine the API

### TODO: 
#   Cache only certain sets of exceptions (determinable by an enumeration)
#   1. when writing code don't catch SyntaxError or TypeError
#   2. when testing code catch these if you don't want to "fail fast"

### Grouped exceptions

# def f():
#     excs = [OSError('error 1'), SystemError('error 2')]
#     raise ExceptionGroup('there were problems', excs)
# 

### except*

# def f():
#     raise ExceptionGroup(
#         "group1",
#         [
#             OSError(1),
#             SystemError(2),
#             ExceptionGroup(
#                 "group2",
#                 [
#                     OSError(3),
#                     RecursionError(4)
#                 ]
#             )
#         ]
#     )
# 
# 
# try:
#     f()
# except* OSError as e:
#     print("There were OSErrors")
# except* SystemError as e:
#     print("There were SystemErrors")
# 
# ### adding notes
# 
# try:
#     raise TypeError('bad type')
# except Exception as e:
#     e.add_note('Add some information')
#     e.add_note('Add some more information')
#     raise
# 
# ### instances, not types
# 
# 
# excs = []
# for test in tests:
#     try:
#         test.run()
#     except Exception as e:
#         excs.append(e)
# 
# if excs:
#    raise ExceptionGroup("Test Failures", excs)
# 
# ### 
# 
# def f():
#     raise OSError('operation failed')
# 
# excs = []
# for i in range(3):
#     try:
#         f()
#     except Exception as e:
#         e.add_note(f'Happened in Iteration {i+1}')
#         excs.append(e)
