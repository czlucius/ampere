import base64
import binascii
from typing import Optional, Callable

from Crypto.Cipher import AES, DES, DES3
from conversions import XToY
from exceptions import CipherError, EncodeDecodeError
from ui.params_info import ParamsInfo


class GenericCipherToByteArray(XToY):
    def __init__(self, val, cipher_creation_callback: Callable, parameters=""):
        super().__init__(val, parameters, self.FROM_UNICODE)
        key = bytes(parameters, encoding="utf-8")
        try:
            self.cipher_obj = cipher_creation_callback(key)
        except ValueError as err:
            raise CipherError(str(err))

    def transform(self):
        try:
            ct = base64.b64decode(self.val)
        except (binascii.Error, ValueError) as err:
            raise EncodeDecodeError(str(err))
        try:
            plaintext = bytes(self.cipher_obj.decrypt(ct))
        except ValueError as err:
            raise CipherError(str(err))  # the built-in error messages look presentable to show on Discord.
        return plaintext

    @staticmethod
    def uses_params():
        return True

    @staticmethod
    def param_info() -> Optional[ParamsInfo]:
        return ParamsInfo("Key")  # TODO: add option to add IV in the future.


class AESECBToByteArray(GenericCipherToByteArray):
    def __init__(self, val, parameters=""):
        super().__init__(val, lambda key: AES.new(key, AES.MODE_ECB), parameters)


class DESECBToByteArray(GenericCipherToByteArray):
    def __init__(self, val, parameters=""):
        super().__init__(val, lambda key: DES.new(key, DES.MODE_ECB), parameters)


class DES3ECBToByteArray(GenericCipherToByteArray):
    def __init__(self, val, parameters=""):
        super().__init__(val, lambda key: DES3.new(key, DES.MODE_ECB), parameters)
