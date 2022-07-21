import base64, base58, base62

from typing import Callable
from main.conversions import XToY


class ByteArrayToBaseEncoded(XToY):
    def __init__(self, val, function: Callable):
        super().__init__(val)
        self.function = function

    def transform(self):
        val = self.val.strip()
        return self.function(val).decode("utf-8")

    def get_type(self) -> int:
        return self.TO_UNICODE


class ByteArrayToBase32(ByteArrayToBaseEncoded):
    def __init__(self, val):
        super().__init__(val, base64.b32encode)


class ByteArrayToBase58(ByteArrayToBaseEncoded):
    def __init__(self, val):
        super().__init__(val, base58.b58encode)


class ByteArrayToBase62(ByteArrayToBaseEncoded):
    def __init__(self, val):
        super().__init__(val, lambda barr: bytes(base62.encodebytes(barr), encoding="utf-8"))


class ByteArrayToBase64(ByteArrayToBaseEncoded):
    def __init__(self, val):
        super().__init__(val, base64.b64encode)


class ByteArrayToAscii85(ByteArrayToBaseEncoded):
    def __init__(self, val):
        super().__init__(val, base64.a85encode)
