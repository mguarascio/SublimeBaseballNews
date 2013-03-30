import sublime
import sublime_plugin
from lib import holycow

'''
TODO:
config - apikey, favorite team

additional features - latest scores in status bar
'''

apikey = '7rjyq97u3smpqbb948prjk7w'
api = holycow.API(apikey)
teamlinkcache = {}


class BaseballNewsCommand(sublime_plugin.WindowCommand):

    def run(self):
        sublime.status_message("Loading baseball news...")
        news = api.team_news('NYY')
        self.newsData = [{'headline': story.headline, 'link': story.links['web']['href']} for story in news]
        self.window.show_quick_panel([[story['headline'], story['link']] for story in self.newsData], self.onUserChoiceSelect)

    def onUserChoiceSelect(self, index):
        if (index != -1):
            self.openURL(self.newsData[index]['link'])

    def openURL(self, url):
        import webbrowser
        webbrowser.open(url)


class BaseballScoresCommand(sublime_plugin.WindowCommand):
    def run(self):
        scores = api.latest_events()
        self.output = []
        for game in scores:
            for abr, homeAway in game.teams.items():
                if homeAway == 'home':
                    print abr
                    link = ''
                    if abr in teamlinkcache.keys():
                        link = teamlinkcache[abr]
                    else:  # Please forgive me...
                        try:
                            team = api.team(abr)
                            link = team.links['web']['teams']['href']
                            print link
                            teamlinkcache[abr] = link
                        except:
                            print 'some exception'
                    self.output.append([game.latest_score(), abr])
                    break
        #     homeTeam = game.teams['home']
        #     self.output.append([game.latest_score(), homeTeam])
        # print 'yes'
        #self.scoresData = [ for game in scores]
        #self.window.show_quick_panel([[game.latest_score(), str(game.id)] for game in scores], self.onUserChoiceSelect)
        self.window.show_quick_panel(self.output, self.onUserChoiceSelect)

    def onUserChoiceSelect(self, index):
        # do something awesome.
        if (index != -1):
            try:
                url = teamlinkcache[self.output[index][1]]
                self.openURL(url)
            except:
                print 'unable to get url'

    def openURL(self, url):
        import webbrowser
        webbrowser.open(url)


class BaseballScoresListener(sublime_plugin.EventListener):
    def __init__(self):
        self.teamAbbr = 'NYY'

    def on_post_save(self, view):
        sublime.set_timeout(self.update_game_status, 3)

    def update_game_status(self):
        favorite_score = api.event_score('320901110')  # doh.
        # connection handling improvements needed!
        latest_score = favorite_score.latest_score()
        sublime.status_message("Latest game update: " + latest_score)
