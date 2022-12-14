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

import base64, base58, base62, base45
import logging
import binascii

from typing import Callable
from components.conversions import XToY
from exceptions import EncodeDecodeError


class BaseEncodedToByteArray(XToY):
    def __init__(self, val, function: Callable, *args, **kwargs):
        super().__init__(val, *args, **kwargs)

        def fn(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except (binascii.Error, ValueError) as exc:
                logging.info(f"BaseEncodedToByteArray: error occurred: {str(exc)}")
                raise EncodeDecodeError(str(exc))

        self.function = fn

    def transform(self):
        val = self.val.strip()
        return self.function(val)

    def get_type(self) -> int:
        return self.FROM_UNICODE


class Base32ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base64.b32decode)

class Base45ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base45.b45decode)


class Base58ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base58.b58decode)


class Base62ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base62.decodebytes)


class Base64ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base64.b64decode)


class Ascii85ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base64.a85decode)
