"""patchpyro - A monkeypatcher add-on for Pyrogram
Copyright (C) 2026 Aditya Prasad S <https://github.com/adityaprasad502>.

This file is part of patchpyro and was forked from usernein/pyromod.

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


__version__ = "2.1.2"
# change in setup.py aswell

from . import listen


def thank() -> None:
    """A dummy function to prevent patchpyro from being removed by formatters and linters. It does nothing, just prints a message to the console to indicate that patchpyro is not an unused import."""
    # print("Thank you for using patchpyro! If you see this message. author: a.devh.in, version: " + __version__)
