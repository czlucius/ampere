"""
A simple object to store info for parameters.
"""
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

from discord import InputTextStyle


class ParamsInfo:
    def __init__(self, name: str,
                 placeholder: str = None,
                 min_length: int = None,
                 max_length: int = None,
                 required: bool = True,
                 prefilled_value: str = None,
                 style: InputTextStyle = InputTextStyle.short,
                 additional_params: list = None):
        self.name, self.style, self.placeholder, self.min_length, self.max_length, self.required, self.prefilled_value, self.additional_params \
            = name, style, placeholder, min_length, max_length, required, prefilled_value, additional_params