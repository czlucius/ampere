import re

from main.conversions import XToY
from main.exceptions import InvalidExpressionException
from main.utils.base import base_arb_to_bytes


class NumericBaseToByteArray(XToY):

    def __init__(self, val, group_len: int, valid_chars_regex: str, base: int):
        super().__init__(val)
        self.group_len = group_len
        self.valid_chars_regex = valid_chars_regex
        self.base = base

    def transform(self):
        val = str(self.val).replace(" ", "").lower()

        invalid_reason = None
        if len(val) % self.group_len != 0:
            # Not in groups of 8
            invalid_reason = f"Pattern is not in groups of {self.group_len}."
        elif re.match(rf"^{self.valid_chars_regex}+$", val) is None:
            invalid_reason = "Pattern contains invalid characters."

        if not invalid_reason:
            # Binary pattern is valid. Perform conversion.
            return base_arb_to_bytes(val, self.base)
        else:
            raise InvalidExpressionException(invalid_reason)

    def get_type(self) -> int:
        return self.FROM_UNICODE
