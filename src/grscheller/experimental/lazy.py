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

* **class Lazy01:** Delayed nullary function evaluation of a single variable
* **class Lazy:** Delay function evaluation of a function taking one argument

"""
from __future__ import annotations

__all__ = [ 'Lazy11', 'Lazy01' ]

from typing import Callable, Iterator
from grscheller.fp.err_handling import MB, XOR

class Lazy11[D, R]():
    """Delayed evaluation of a function taking and returning single values.

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
    * class is iterable and callable with no arguments
      * if needed, will first evaluate `f` with its arguments
      * if not successful raise a RunTimeError
        * guard against this by
          * first calling the eval method
          * then testing the Lazy object itself in a Boolean context

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances.
    """

    __slots__ = '_f', '_arg', '_result', '_pure'

    def __init__(self, f: Callable[[D], R], arg: D, pure: bool=True) -> None:
        self._f = f
        self._arg = arg
        self._pure = pure
        self._result: XOR[R, MB[Exception]] = XOR(MB(), MB())

    def __bool__(self) -> bool:
        return True if self._result else False

    def is_evaluated(self) -> bool:
        return self._result != XOR(MB(), MB())

    def is_exceptional(self) -> bool:
        if self.is_evaluated():
            return False if self._result else True
        else:
            return False

    def is_pure(self) -> bool:
        return self._pure

    def eval(self) -> bool:
        """Evaluate function with its arguments.

        * evaluate function
        * cache results or exceptions

        """
        if not self.is_evaluated() or not self._pure:
            try:
                result = self._f(self._arg)
            except Exception as exc:
                self._result = XOR(MB(), MB(exc))
                return False
            else:
                self._result = XOR(MB(result), MB())

        return True

    def result(self) -> MB[R]:
        if not self.is_evaluated():
            self.eval()

        if self._result:
            return MB(self._result.getLeft())
        else:
            return MB()

    def exception(self) -> MB[Exception]:
        if not self.is_evaluated():
            self.eval()

        return self._result.getRight()

class Lazy01[R](Lazy11[None, R]):
    """Delayed evaluation of a nullary function returning a single value.

    Class instance delays the executable of a nullary function where `Lazy01(f)`
    constructs an object that can evaluate the Callable `f: Callable[[]. r]`
    at a later time.

    * argument `f` takes a function taking no arguments
    * function is evaluated when the eval method is called
      * self._results set to `XOR[~R, MB[Exception]]`
      * where `~R` is the return type of `f`, possibly `None`
    * result is cached unless `pure` is set to `False` in `__init__` method
    * class is callable and iterable
      * if needed, will first evaluate `f`
      * if not successful raise a RunTimeError
        * guard against this by
          * first calling the eval method
          * then testing the Lazy object itself in a Boolean context

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances.
    """
    def __init__(self, f: Callable[[], R], pure: bool=True) -> None:
        super().__init__(lambda n: f(), arg=None, pure=pure)

