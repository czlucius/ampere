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

class InvalidExpressionException(Exception):
    pass

class TimeoutException(Exception):
    pass

class FieldTooLongError(Exception):
    pass

class InputInvalidException(Exception):
    pass

class EncodeDecodeError(Exception):
    pass

class InvalidParametersException(InputInvalidException):
    pass

class CipherError(Exception):
    pass

class CodeRunnerException(Exception):
    pass

class InvalidOptionException(Exception):
    pass