# Copyright (C) 2022 David Spencer
#
# This file is part of LPM.
#
# LPM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LPM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LPM.  If not, see <http://www.gnu.org/licenses/>.

from random import randint


class Key:
    """Representation of your encryption key."""

    as_bytes: bytes

    def __init__(self, __bytes: bytes | None) -> None:
            self.as_bytes = self.gen() if __bytes is None else __bytes

    def gen(self):
        """Generates a random key."""

        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+{[}];:'\"|\\<>,./?"
        key = ""

        for _ in range(randint(10, 50)): key += chars[randint(0, len(chars)-1)]
        return bytes(key + "\n", encoding="ascii")
