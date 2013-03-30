import requests
import json
from team import Team
from news import News
from scores import EventScore


class API(object):

    def __init__(self, api_key,
                       urlroot='http://api.espn.com',
                       version='v1',
                       api_root='sports/baseball/mlb'
                       ):
        self.api_key = api_key
        self.urlroot = urlroot
        self.version = version
        self.api_root = api_root
        self.enables = ['venues']

    def teams(self):
        ''' Return all MLB teams as a list of Team objects '''
        method = 'teams'
        response = self.__request(method)
        teams = []
        data = response['sports'][0]['leagues'][0]
        for raw_team in data['teams']:
            teams.append(Team(raw_team))
        return teams

    def team(self, abbr=None, id=None):
        ''' Lookup a team by abbreviation, or by id e.g. API.team(abbr='NYY') or API.team(id=1) '''
        team_id = id
        if abbr and abbr in API.team_ids:
            team_id = API.team_ids[abbr]
        if team_id is None or team_id < 1:
            raise ValueError("Invalid id or abbr: [abbr] = " + abbr + ", [id] = " + id)

        method = ''.join(['teams/', str(team_id)])
        response = self.__request(method)
        data = response['sports'][0]['leagues'][0]
        return Team(data['teams'][0])

    def news(self):
        ''' Top MLB news '''
        method = 'news'
        response = self.__request(method)
        news = []
        for raw_news in response['headlines']:
            news.append(News(raw_news))
        return news

    def team_news(self, abbr):
        ''' MLB news for a specific team '''
        method = 'news'
        if abbr and abbr in API.team_ids:
            team_id = API.team_ids[abbr]

        if team_id:
            method = ''.join(['teams/', str(team_id), '/news'])
        else:
            raise ValueError("Invalid team abbr: " + abbr)

        response = self.__request(method)
        news = []
        for raw_news in response['headlines']:
            news.append(News(raw_news))

        return news

    # TODO: this is silly to have so much duplicated events code
    def latest_events(self):
        ''' Scores data for all recent games '''
        method = 'events'
        response = self.__request(method)
        scores = []
        data = response['sports'][0]['leagues'][0]['events']
        for raw_scores in data:
            competition = raw_scores['competitions'][0]
            scores.append(EventScore(competition))

        return scores

    def event_score(self, event_id):
        ''' Scores data for a given eventid '''
        method = ''.join(['events/', str(event_id)])
        response = self.__request(method)
        scores = []
        data = response['sports'][0]['leagues'][0]['events'][0]
        for raw_scores in data['competitions']:
            scores.append(EventScore(raw_scores))

        return scores[0]

    def __request(self, method):
        url = ''.join([self.urlroot, '/',
                       self.version, '/',
                       self.api_root, '/',
                       method,
                       '?apikey=', self.api_key,
                       '&enable=', ','.join(self.enables)])
        r = requests.get(url, timeout=3)
        response = json.loads(r.text)
        return response

    team_ids = {
        'BAL': 1,
        'BOS': 2,
        'LAA': 3,
        'CHW': 4,
        'CLE': 5,
        'DET': 6,
        'KC': 7,
        'MIL': 8,
        'MIN': 9,
        'NYY': 10,
        'OAK': 11,
        'SEA': 12,
        'TEX': 13,
        'TOR': 14,
        'ATL': 15,
        'CHC': 16,
        'CIN': 17,
        'HOU': 18,
        'LAD': 19,
        'WSH': 20,
        'NYM': 21,
        'PHI': 22,
        'PIT': 23,
        'STL': 24,
        'SD': 25,
        'SF': 26,
        'COL': 27,
        'MIA': 28,
        'ARI': 29,
        'TB': 30
        }
