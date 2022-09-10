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

import abc
from typing import Optional

from models.params_info import ParamsInfo


class XToY(abc.ABC):
    FROM_UNICODE = 0
    TO_UNICODE = 1
    OTHER_CONV = 2

    """
    parameters:
    Please supply a list of 
    """

    def __init__(self, val, parameters=None, _type=OTHER_CONV):
        self.val = val
        self.parameters = parameters
        self._type = _type

    @abc.abstractmethod
    def transform(self):
        pass

    def get_type(self) -> int:
        return self._type

    def has_params(self):
        return self.parameters is not None

    @staticmethod
    def uses_params():
        return False  # Only classes which have parameters should set this to True.

    """
    Get info on parameter accepted.
    Will be returned as an object.
    Info must be of type ParamsInfo.
    """
    @staticmethod
    def param_info() -> Optional[ParamsInfo]:
        return None