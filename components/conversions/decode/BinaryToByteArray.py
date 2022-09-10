#   A multi-purpose Discord Bot written with Python and pycord.
#   Copyright (C) 2022 czlucius (lcz5#3392)
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

from components.conversions import XToY
from exceptions import InvalidExpressionException
from functions.base import bitstring_to_bytes


class BinaryToByteArray(XToY):
    def transform(self):
        # Convert from Binary to Byte Array.
        val = str(self.val).replace(" ", "")
        # print(val)

        invalid_reason = None
        if len(val) % 8 != 0:
            # Not in groups of 8
            invalid_reason = "Binary pattern is not in groups of 8."
        elif re.match("^[01]+$", val) is None:
            invalid_reason = "Binary pattern contains characters other than 0 or 1"

        if not invalid_reason:
            # Binary pattern is valid. Perform conversion.
            return bitstring_to_bytes(val)
        else:
            raise InvalidExpressionException(invalid_reason)

    def get_type(self) -> int:
        return self.FROM_UNICODE
