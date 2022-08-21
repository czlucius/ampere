import logging

from main.conversions import XToY
from Crypto.Hash import SHA256, MD5, SHA1, SHA512


class ByteArrayToGenericHash(XToY):
    def __init__(self, val, hashing_cls):
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
    def __init__(self, val):
        super().__init__(val, SHA256)

class ByteArrayToMD5(ByteArrayToGenericHash):
    def __init__(self, val):
        super().__init__(val, MD5)

class ByteArrayToSHA1(ByteArrayToGenericHash):
    def __init__(self, val):
        super().__init__(val, SHA1)

class ByteArrayToSHA512(ByteArrayToGenericHash):
    def __init__(self, val):
        super().__init__(val, SHA512)