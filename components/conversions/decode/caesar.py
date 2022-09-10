#   A multi-purpose Discord Bot written with Python and pycord.
#   Copyright (C) 2022 czlucius (lcz5#3392)
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import Optional

from components.conversions import XToY
from exceptions import InvalidParametersException
from models.params_info import ParamsInfo

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class CaesarCipherToByteArray(XToY):

    def __init__(self, val, parameters):
        super().__init__(val, parameters, _type=XToY.FROM_UNICODE)

    def transform(self):
        logging.info(f"CaesarCipherToByteArray - {self.val}, params = {self.parameters}")
        val = str(self.val)
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
                converted = alphabet[(alphabet.index(char.upper()) - shift) % len(alphabet)] # Just overflow if >26 or <-26.
                converted = converted if case else converted.lower()
            else:
                converted = char
            new += converted

        new_bytes = bytes(new, encoding="utf-8")
        return new_bytes


    @staticmethod
    def uses_params():
        return True

    @staticmethod
    def param_info() -> Optional[ParamsInfo]:
        return ParamsInfo("Shift", min_length=1)