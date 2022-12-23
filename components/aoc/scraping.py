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
import os

import aiohttp
from bs4 import BeautifulSoup

from exceptions import ChallengeUnavailableException

from dotenv import load_dotenv

load_dotenv("secret.env")
AOC_TOKEN = os.getenv("AOC_API_KEY")
headers = {
    'User-Agent': 'Mozilla/5.0 AmpereBot/1.0 - (Ampere by lucius@czlucius.dev, github.com/czlucius/ampere)'
}

cookies = {
    'session': AOC_TOKEN
}


async def scrape_challenge(year: int, day: int, part: int) -> str:
    # We do not want to excessively scrape the AoC servers, so we shall cache the HTML response.
    contents = ""

    cache_file_path = f".amperecache/aoc/challenge/aoc{year}{day}{part}"
    if os.path.exists(cache_file_path):
        # HTML has been cached.
        with open(cache_file_path) as f:
            html = f.read()
    else:
        url = f"https://adventofcode.com/{year}/day/{day}"
        async with aiohttp.ClientSession().get(url, headers=headers, cookies=cookies) as response:
            html = await response.text()
        os.makedirs(".amperecache/aoc/challenge/", exist_ok=True)
        with open(cache_file_path, "w") as f:
            f.write(html)
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article")
    if len(articles) < 2 and part == 2:
        os.remove(cache_file_path)
        raise ChallengeUnavailableException("Part 2 is not yet available")
    contents = str(articles[part - 1])
    return contents
