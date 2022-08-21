import logging
from typing import Optional

from main.conversions import XToY
from main.exceptions import InvalidParametersException, InputInvalidException
from main.ui.params_info import ParamsInfo

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ByteArrayToCaesarCipher(XToY):

    def __init__(self, val, parameters):
        super().__init__(val, parameters, _type=XToY.FROM_UNICODE)

    def transform(self):
        logging.info(f"ByteArrayToCaesarCipher - {self.val}, params = {self.parameters}")
        val = self.val.decode("utf-8")
        # The key, as in how many characters to shift.
        shift = self.parameters
        try:
            shift = int(shift)
        except ValueError:
            raise InvalidParametersException("Shift is not an integer.")

        new = ""
        for char in val:
            logging.info(f"char in val: {char}")
            if char.isalpha():
                case = char.isupper()
                converted = alphabet[(alphabet.index(char.upper()) + shift) % len(alphabet)] # Just overflow if >26 or <-26.
                converted = converted if case else converted.lower()
            else:
                converted = char
            new += converted


        return new


    @staticmethod
    def uses_params():
        return True

    @staticmethod
    def param_info() -> Optional[ParamsInfo]:
        return ParamsInfo("Shift", min_length=1)