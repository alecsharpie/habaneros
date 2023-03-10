import requests
from bs4 import BeautifulSoup

import os

from futsal.utils import _filter_team_of_interest
from futsal.data import get_history
from futsal.parser import parse_history

class HomeTeam:
    def __init__(self, team_name, base_url):
        self.team_name = team_name
        self.base_url = base_url
        self.games = self.all_games()
        # self.next_opponent = self.next_opponent()

    def all_games(self):

        games_list = []

        for round_id in range(1, 14):

            params = {'r': round_id,
            'd': 15983}

            html = requests.get(self.base_url, params).content

            soup = BeautifulSoup(html, 'html.parser')

            game = _filter_team_of_interest(soup, self.team_name)

            if game:
                games_list.append(game)

        return games_list

    def future_games(self):
        return [game for game in self.games if game['Result'] is None]

    def past_games(self):
        return [game for game in self.games if game['Result'] is not None]

    def next_game(self):

        future = self.future_games()

        if len(future) > 0:
            return future[0]
        else:
            return None

    def next_opponent(self):

        upcoming_team_link = self.next_game().get('Opponent').get('url')

        opponent_past_games = parse_history(get_history(upcoming_team_link))

        return opponent_past_games


    def future_opponents(self):

        future_opponents_past_games = [parse_history(get_history(game.get('Opponent').get('url'))) for game in self.future_games()]

        return future_opponents_past_games


    def foresight(self):

        for opponent, game in zip(self.future_opponents(), self.future_games()):
            game['Opponent']['history'] = opponent

        return self.future_games()
