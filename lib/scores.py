

class EventScore():
    ''' Only available via partner api. Very much a WIP for @baseballhackday....
        (aka, it's ugly)
    '''
    def __init__(self, results):
        self.id = results['id']
        self.date = results['date']
        self.competitors = results['competitors']
        # STARTING UGLY CODE...some competitor records don't have a name...figure it out later, future Mike.
        self.score = dict([(competitor['team']['name'], competitor['score']) for competitor in self.competitors if 'name' in competitor['team'].keys()])        
        self.teams = dict([(competitor['team']['abbreviation'], competitor['homeAway']) for competitor in self.competitors if 'abbreviation' in competitor['team'].keys()])        
        # ENDING UGLY CODE. Actually, there's more elsewhere...
        self.inning = results['period']
        self.status = results['status']['detail']

    def latest_score(self):
        message = u''
        for k, v in self.score.iteritems():
            message = ''.join([message, u' {0}: {1}'.format(k, str(v))])
        message = ', '.join([message, self.status])

        return message
