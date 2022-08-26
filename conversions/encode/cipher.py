import base64
import binascii
from typing import Optional, Callable

from Crypto.Cipher import AES, DES, DES3
from conversions import XToY
from exceptions import CipherError, EncodeDecodeError
from ui.params_info import ParamsInfo

# TODO work needs to be done for padding for AES ECB encryption.
class ByteArrayToGenericCipher(XToY):
    def __init__(self, val, cipher_creation_callback: Callable, parameters=""):
        super().__init__(val, parameters, self.TO_UNICODE)
        key = bytes(parameters, encoding="utf-8")
        try:
            self.cipher_obj = cipher_creation_callback(key)
        except ValueError as err:
            raise CipherError(str(err))

    def transform(self):
        # try:
        #     ct = base64.b64decode(self.val)
        # except (binascii.Error, ValueError) as err:
        #     raise EncodeDecodeError(str(err))
        plaintext = self.val
        try:
            ct = self.cipher_obj.encrypt(plaintext)
        except ValueError as err:
            raise CipherError(str(err))  # the built-in error messages look presentable to show on Discord.
        try:
            formatted_ct = base64.b64encode(ct)
        except (ValueError, binascii.Error) as err:
            raise EncodeDecodeError(str(err))

        return formatted_ct.decode("utf-8")

    @staticmethod
    def uses_params():
        return True

    @staticmethod
    def param_info() -> Optional[ParamsInfo]:
        return ParamsInfo("Key")  # TODO: add option to add IV in the future.


class ByteArrayToAESECB(ByteArrayToGenericCipher):
    def __init__(self, val, parameters=""):
        super().__init__(val, lambda key: AES.new(key, AES.MODE_ECB), parameters)


class ByteArrayToDESECB(ByteArrayToGenericCipher):
    def __init__(self, val, parameters=""):
        super().__init__(val, lambda key: DES.new(key, DES.MODE_ECB), parameters)


class ByteArrayToDES3ECB(ByteArrayToGenericCipher):
    def __init__(self, val, parameters=""):
        super().__init__(val, lambda key: DES3.new(key, DES.MODE_ECB), parameters)
