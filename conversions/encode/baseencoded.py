import base64, base58, base62, base45
import logging
import binascii

from typing import Callable
from conversions import XToY
from exceptions import EncodeDecodeError


class ByteArrayToBaseEncoded(XToY):
    def __init__(self, val, function: Callable, *args, **kwargs):
        super().__init__(val)

        def fn(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except (binascii.Error, ValueError) as exc:
                logging.info(f"BaseEncodedToByteArray: error occurred: {str(exc)}")
                raise EncodeDecodeError(str(exc))

        self.function = fn

    def transform(self):
        val = self.val.strip()
        return self.function(val).decode("utf-8")

    def get_type(self) -> int:
        return self.TO_UNICODE


class ByteArrayToBase32(ByteArrayToBaseEncoded):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base64.b32encode)

class ByteArrayToBase45(ByteArrayToBaseEncoded):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base45.b45encode)


class ByteArrayToBase58(ByteArrayToBaseEncoded):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base58.b58encode)


class ByteArrayToBase62(ByteArrayToBaseEncoded):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, lambda barr: bytes(base62.encodebytes(barr), encoding="utf-8"))


class ByteArrayToBase64(ByteArrayToBaseEncoded):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base64.b64encode)


class ByteArrayToAscii85(ByteArrayToBaseEncoded):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, base64.a85encode)
