import base64, base58, base62

from typing import Callable
from main.conversions import XToY


class BaseEncodedToByteArray(XToY):
    def __init__(self, val, function: Callable):
        super().__init__(val)
        self.function = function

    def transform(self):
        val = self.val.strip()
        return self.function(val)

    def get_type(self) -> int:
        return self.FROM_UNICODE


class Base32ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val):
        super().__init__(val, base64.b32decode)


class Base58ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val):
        super().__init__(val, base58.b58decode)


class Base62ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val):
        super().__init__(val, base62.decodebytes)


class Base64ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val):
        super().__init__(val, base64.b64decode)


class Ascii85ToByteArray(BaseEncodedToByteArray):
    def __init__(self, val):
        super().__init__(val, base64.a85decode)
