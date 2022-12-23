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
import typing
from typing import Dict

import pymongo
from dotenv import load_dotenv

from exceptions import AoCAlreadySolved

load_dotenv("secret.env")
url = os.getenv("AOC_LEADERBOARD_DB_URL")

# Create a connection to the MongoDB server
client = pymongo.MongoClient(url)

# Get the "server" collection
servers_db = client['leaderboard']
servers_collection = servers_db['server']


class Server:
    def __init__(self, server_id: int, populate: bool = False, autosave: bool = True):
        self.server_id = server_id
        self.leaderboard = {}
        self.autosave = autosave
        if populate:
            self.refresh_destructive()

    @property
    def state(self) -> Dict[str, typing.Any]:
        print({
            "server_id": self.server_id,
            "leaderboard": self.leaderboard
        })
        return {
            "server_id": self.server_id,
            "leaderboard": self.leaderboard
        }

    def create_user(self, user: str):
        """Creates a new user in the leaderboard with an empty list for their challenges."""
        if user not in self.leaderboard:
            self.leaderboard[user] = []

        if self.autosave:
            self.save()

    def update_challenges(self, user: str, challenges: list, create_if_missing: bool = True):
        """Updates the challenges for a given user."""
        if user in self.leaderboard:
            self.leaderboard[user] = challenges
        else:
            if create_if_missing:
                self.leaderboard[user] = challenges
            else:
                raise ValueError(f"User {user} does not exist in the leaderboard.")
        if self.autosave:
            self.save()

    def add_challenge(self, user: str, challenge: str, create_if_missing: bool = True):
        """Adds a challenge to the challenges of a given user. This method is idempotent."""
        print("wgwgwg")
        if user in self.leaderboard:
            if challenge not in self.leaderboard[user]:
                self.leaderboard[user].append(challenge)
            else:
                raise AoCAlreadySolved("You already solved this challenge!")
        else:
            if create_if_missing:
                self.leaderboard[user] = [challenge]
            else:
                raise ValueError(f"User {user} does not exist in the leaderboard.")
        if self.autosave:
            self.save()

    def get_challenges(self, user: str, err_if_not_exist: bool = False) -> list:
        """Returns the challenges for a given user."""
        print(self.leaderboard)
        if user in self.leaderboard:
            return self.leaderboard[user]
        else:
            if err_if_not_exist:
                raise ValueError(f"User {user} does not exist in the leaderboard.")
            else:
                self.create_user(str(user))
                return []

    def get_top_10(self) -> list:
        users = self.leaderboard.keys()
        print(users)
        """Returns the top 10 users in the leaderboard based on the length of their challenges list."""
        # Sort the leaderboard by the length of the challenges list
        sorted_leaderboard = sorted(users, key=lambda key: len(self.leaderboard[key]), reverse=True)

        # Return the top 10 users
        return sorted_leaderboard[:10]

    def get_user_score(self, user: str) -> int:
        try:
            return len(self.leaderboard[user])
        except KeyError:
            return 0

    def save(self):
        """Saves the server object to the MongoDB collection."""
        servers_collection.replace_one({'server_id': self.server_id}, self.state, upsert=True)

    def refresh_destructive(self) -> bool:
        server_data = servers_collection.find_one({'server_id': self.server_id})
        if server_data:
            self.state.update(server_data)
            return True
        else:
            return False

    @classmethod
    def load(cls, server_id: int):
        """Loads a server object from the MongoDB collection."""
        server_data = servers_collection.find_one({'server_id': server_id})
        print(server_data)
        server = Server(server_id)

        if server_data:
            server.server_id = server_data["server_id"]
            server.leaderboard = server_data["leaderboard"]
        else:
            servers_collection.insert_one({
                "server_id": server_id,
                "leaderboard": {}
            })
        return server

    @staticmethod
    def get_challenge_identifier(year, day, part):
        return f"aoc{year}{day}{part}"

