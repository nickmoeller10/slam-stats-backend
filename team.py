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
        # Check if 'valuesByStat' exists and assign 0 if not
        values_by_stat = team.get('valuesByStat', {})

        self.points = values_by_stat.get('0', 0)
        self.blocks = values_by_stat.get('1', 0)
        self.steals = values_by_stat.get('2', 0)
        self.assists = values_by_stat.get('3', 0)
        self.rebounds = values_by_stat.get('6', 0)
        self.games = values_by_stat.get('42', 0)
        self.turnovers = values_by_stat.get('11', 0)
        self.fgm = values_by_stat.get('13', 0)
        self.fga = values_by_stat.get('14', 0)
        self.ftm = values_by_stat.get('15', 0)
        self.fta = values_by_stat.get('16', 0)
        self.threePointersMade = values_by_stat.get('17', 0)
        self.fgp = values_by_stat.get('19', 0)
        self.ftp = values_by_stat.get('20', 0)

        # self.points = team['valuesByStat']['0']
        # self.blocks = team['valuesByStat']['1']
        # self.steals = team['valuesByStat']['2']
        # self.assists = team['valuesByStat']['3']
        # self.rebounds = team['valuesByStat']['6']
        # self.games = team['valuesByStat']['42']
        # self.turnovers = team['valuesByStat']['11']
        # self.fgm = team['valuesByStat']['13']
        # self.fga = team['valuesByStat']['14']
        # self.ftm = team['valuesByStat']['15']
        # self.fta = team['valuesByStat']['16']
        # self.threePointersMade = team['valuesByStat']['17']
        # self.fgp = team['valuesByStat']['19']
        # self.ftp = team['valuesByStat']['20']
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
