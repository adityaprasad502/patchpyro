"""patchpyro - A monkeypatcher add-on for Pyrogram
Copyright (C) 2026 Aditya Prasad S <https://github.com/adityaprasad502>.

This file is part of patchpyro and was forked from usernein/pyromod.
Additional patching logic was adapted from kurimod (C) Dias Arthur.

patchpyro is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

patchpyro is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with patchpyro.  If not, see <https://www.gnu.org/licenses/>.
"""
from collections.abc import Callable
from contextlib import asynccontextmanager, contextmanager
from inspect import iscoroutinefunction
from typing import TypeVar

from pyrogram.sync import async_to_sync

T = TypeVar("T")


def patch(target_class):
    def is_patchable(item):
        func = item[1]
        return getattr(func, "should_patch", False) or getattr(func, "patchable", False)

    def wrapper(container: type[T]) -> T:
        for name, func in filter(is_patchable, container.__dict__.items()):
            old = getattr(target_class, name, None)
            if old is not None:
                setattr(target_class, "old" + name, old)

            tempConf = {
                i: getattr(func, i, False)
                for i in ["is_property", "is_static", "is_context"]
            }

            if not iscoroutinefunction(func):
                async_to_sync(container, name)
                func = getattr(container, name)

            for tKey, tValue in tempConf.items():
                setattr(func, tKey, tValue)

            if func.is_property:
                func = property(func)
            elif func.is_static:
                func = staticmethod(func)
            elif func.is_context:
                if iscoroutinefunction(func.__call__):
                    func = asynccontextmanager(func)
                else:
                    func = contextmanager(func)

            setattr(target_class, name, func)
        return container

    return wrapper


def patchable(
    func: Callable | None = None,
    *,
    is_property: bool = False,
    is_static: bool = False,
    is_context: bool = False,
) -> Callable:
    def wrapper(f: Callable) -> Callable:
        f.should_patch = True
        f.patchable = True
        f.is_property = is_property
        f.is_static = is_static
        f.is_context = is_context
        return f

    if func is not None:
        return wrapper(func)
    return wrapper


patch_into = patch
should_patch = patchable
