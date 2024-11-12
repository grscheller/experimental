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

#### Non-strict delayed function evaluation:

* class **Lazy:** Delay evaluation of function taking & returning single values
* class **Lazy01:** Delay evaluation of nullary function returning a single value
* class **Lazy10:** Delay evaluation of function taking a single value & returning no values
* class **Lazy00:** Delay evaluation of function neither taking nor returning any values
* function **lazy:** Delay evaluation of a function taking more than one value

"""
from __future__ import annotations

__all__ = [ 'Lazy11', 'Lazy01', 'Lazy10', 'Lazy00' ]

from typing import Any, Callable, cast, Final, Iterator
from grscheller.fp.err_handling import MB, XOR

class Lazy[D, R]():
    """Delayed evaluation of a function taking and returning single values.

    Class instance delays the executable of a function where `Lazy(f, arg)`
    constructs an object that can evaluate the Callable `f` with its argument
    at a later time.

    * first argument `f` takes a function of 1 argument
    * second argument `args` is the argument to be passed to `f`
      * where the type `~D` is the `tuple` type of the argument types to `f`
    * function is evaluated when the eval method is called
    * result is cached unless `pure` is set to `False` in `__init__` method

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances.
    """

    __slots__ = '_f', '_arg', '_result', '_pure'

    def __init__(self, f: Callable[[D], R], arg: D, pure: bool=True) -> None:
        self._f: Final[Callable[[D], R]] = f
        self._arg: Final[D] = arg
        self._pure: Final[bool] = pure
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
        """Evaluate function with its argument.

        * evaluate function
        * cache results or exceptions if `pure == True`
        * reevaluate if `pure == False`

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
        if self:
            return True
        else:
            return False

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

class Lazy01[R](Lazy[None, R]):
    """Delayed evaluation of a nullary function returning a single value.

    Class instance delays the executable of a nullary function where `Lazy01(f)`
    constructs an object that can evaluate the Callable `f: Callable[[], R]`
    at a later time.

    * argument `f` takes a function taking no arguments
    * function is evaluated when the eval method is called
    * result is cached unless `pure` is set to `False`

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances.
    """
    def __init__(self, f: Callable[[], R], pure: bool=True) -> None:
        super().__init__(lambda _: f(), arg=None, pure=pure)

class Lazy10[D](Lazy[D, None]):
    """Delayed evaluation of a one argument function returning None.

    Class instance delays the executable of a one argument function which
    returns no values where `Lazy00(f, arg)` constructs an object that
    can evaluate the Callable `f: Callable[[D], None]` with its argument
    at a later time.

    * argument `f` takes a function taking one argument and returnng `None`
    * function is evaluated when the eval method is called
    * result is cached unless `pure` is set to `False`

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances. 
    """
    def __init__(self, f: Callable[[D], None], arg: D, pure: bool=True) -> None:
        super().__init__(f, arg, pure=pure)

class Lazy00(Lazy[tuple[()], None]):
    """Delayed evaluation of a nullary function returning None.

    Class instance delays the executable of a function taking and returning no
    values where `Lazy00(f)` constructs an object that can evaluate the Callable
    `f: Callable[[D]. None]` with its argument at a later time.

    * argument `f` takes a function that only has side effects
    * function is evaluated when the eval method is called
    * result is cached unless `pure` is set to `False`
      * setting `pure` to `True` to "initialize" only once
      * setting `pure` to `False` redo side effects & non-pure function behavior

    Usually use case is to make a function "non-strict" by passing some of its
    arguments wrapped in Lazy instances.
    """
    def __init__(self, f: Callable[[], None], pure: bool=True) -> None:
        super().__init__(lambda _: f(), arg=(), pure=pure)

def lazy[R](f: Callable[[*(tuple[Any, ...])], R],
            args: tuple[*(tuple[Any, ...])],
            pure: bool=True) -> Lazy[Any, R]:
    """Delayed evaluation of a function.

    Function returning a delayed evaluation of a function of an arbitrary number
    of positional arguments.

    * first argument `f` takes a function of a given number of arguments
    * second argument `args` is the tuple of the arguments to be passed to `f`
      * it is the programmer's responsibility to ensure that
        * the types and number of arguments of the tuple are compatible with `f`
    * `f` is evaluated when the returned `eval` method of the returned Lazy is called
    * result is cached unless `pure` is set to `False`

    """
    nargs = len(args)
    if nargs == 0:
        return Lazy01(f, pure)
    elif nargs == 1:
        return Lazy(cast(Callable[[Any], R], f), args[0], pure)
    else:
        def fTupled(f: Callable[[*(tuple[Any, ...])], R],
                    arguments: tuple[*(tuple[Any, ...])]) -> R:
            return f(*arguments)
        return Lazy(cast(Callable[[Any], R], fTupled), args, pure)

