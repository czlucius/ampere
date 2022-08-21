from conversions import XToY
from functions.base import bytes_to_base_arb


class ByteArrayToNumericBase(XToY):

    def __init__(self, val, base: int, *args, **kwargs):
        super().__init__(val)
        self.base = base

    def transform(self):
        # val is given as bytes, so we just have to convert it to an arbitrary base.
        val_conv = bytes_to_base_arb(self.val, self.base)
        return str(val_conv)

    def get_type(self) -> int:
        return self.TO_UNICODE