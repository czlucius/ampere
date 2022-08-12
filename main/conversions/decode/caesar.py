from main.conversions import XToY
from main.exceptions import InvalidParamtersException


class CaesarCipherToByteArray(XToY):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, val, parameters):
        super().__init__(val, parameters, _type=XToY.FROM_UNICODE)

    def transform(self):
        val = str(self.val)
        # The key, as in how many characters to shift.
        shift = self.parameters
        try:
            shift = int(shift)
        except ValueError:
            raise InvalidParamtersException("Shift is not an integer.")
        new = ""
        for char in val:
            case = char.isupper()
            converted = alphabet[(alphabet.index(char.upper()) + shift) % len(alphabet)] # Just overflow if >26 or <-26.
            new += converted

        new_bytes = bytes(new)
        return new_bytes


    @staticmethod
    def uses_params():
        return True
    
    @staticmethod
    def param_name():
        return "Shift"