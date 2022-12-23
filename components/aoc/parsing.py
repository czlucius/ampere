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

def parse_aoc_response(response: str) -> int:
    """
    Parse AoCD response.
    :param response: Response by AoC servers/AoCD

    :return: 1 for correct, 0 for wrong, and -1 for indeterminate, -2 for rate limiting, -3 for invalid input, -4 for internal server error.
    """
    if "That's the right answer" in response:
        return 1
    if "That's not the right answer" in response:
        return 0
    if "You gave an answer too recently" in response:
        return -2

    if "already solved" in response:
        if "with same answer:" in response:
            return 1
        elif "with different answer:" in response:
            return 0

    if "aocd will not submit that answer again" in response:
        return 0

    if "cowardly refusing to" in response:
        return -3

    if "part must be " in response:
        return -3

    if "Did you already complete it" in response:
        return -1  # answer is indeterminate; I do not have a sample response to parse.

    return -1



