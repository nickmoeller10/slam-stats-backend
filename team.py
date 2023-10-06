import json
class team:
    def __init__(self, team):
        self.abbrev = team['abbrev']
        self.playoff_seed = team['playoffSeed']
        self.name = team['name']
        self.id = team['id']
        self.logo = team['logo']
        self.wins = team['record']['overall']['wins']
        self.losses = team['record']['overall']['losses']
        self.ties = team['record']['overall']['ties']
        
        self.percentage = team['record']['overall']['percentage']
        self.points = team['valuesByStat']['0']
        self.blocks = team['valuesByStat']['1']
        self.steals = team['valuesByStat']['2']
        self.assists = team['valuesByStat']['3']
        self.rebounds = team['valuesByStat']['6']
        self.games = team['valuesByStat']['42']
        self.turnovers = team['valuesByStat']['11']
        self.fgm = team['valuesByStat']['13']
        self.fga = team['valuesByStat']['14']
        self.ftm = team['valuesByStat']['15']
        self.fta = team['valuesByStat']['16']
        self.threePointersMade = team['valuesByStat']['17']
        self.fgp = team['valuesByStat']['19']
        self.ftp = team['valuesByStat']['20']
        return

    def __iter__(self):
        yield 'abbrev', self.abbrev
        yield 'playoff_seed', self.playoff_seed
        yield 'name', self.name
        yield 'id', self.id
        yield 'logo', self.logo
        yield 'wins', self.wins
        yield 'losses', self.losses
        yield 'ties', self.ties
        yield 'percentage', self.percentage
        yield 'points', self.points
        yield 'blocks', self.blocks
        yield 'steals', self.steals
        yield 'assists', self.assists
        yield 'rebounds', self.rebounds
        yield 'games', self.games
        yield 'turnovers', self.turnovers
        yield 'fgm', self.fgm
        yield 'fga', self.fga
        yield 'ftm', self.ftm
        yield 'fta', self.fta
        yield 'threePointersMade', self.threePointersMade
        yield 'fgp', self.fgp
        yield 'ftp', self.ftp
