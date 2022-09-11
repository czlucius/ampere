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

import logging

from components.conversions import XToY
from Crypto.Hash import SHA256, MD5, SHA1, SHA512


class ByteArrayToGenericHash(XToY):
    def __init__(self, val, hashing_cls, **kwargs):
        super().__init__(val, _type=XToY.FROM_UNICODE)
        self.hashing_cls = hashing_cls

    def transform(self):
        logging.info(f"ByteArrayToGenericHash - {self.val}")
        val = self.val
        # The key, as in how many characters to shift.
        hash_obj = self.hashing_cls.new(val)
        computed_hash = hash_obj.hexdigest()

        return computed_hash


class ByteArrayToSHA256(ByteArrayToGenericHash):
    def __init__(self, val, **kwargs):
        super().__init__(val, SHA256)

class ByteArrayToMD5(ByteArrayToGenericHash):
    def __init__(self, val, **kwargs):
        super().__init__(val, MD5)

class ByteArrayToSHA1(ByteArrayToGenericHash):
    def __init__(self, val,**kwargs):
        super().__init__(val, SHA1)

class ByteArrayToSHA512(ByteArrayToGenericHash):
    def __init__(self, val, **kwargs):
        super().__init__(val, SHA512)
