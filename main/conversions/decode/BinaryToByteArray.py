import re
import string
from abc import ABC

from main.conversions import XToY
from main.exceptions import InvalidExpressionException
from main.functions.base import bitstring_to_bytes


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
