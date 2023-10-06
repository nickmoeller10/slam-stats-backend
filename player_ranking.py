class player_ranking:
    def __init__(self, entry):
        self.player_id = entry['player']['id']
        self.name = entry['player']['fullName']
        self.team = entry['player']['proTeamId']
        self.on_team_id = entry['onTeamId']
        self.position = entry['player']['defaultPositionId']
        self.injury_status = entry['player']['injuryStatus']
        self.stats = entry['playerPoolEntry']['player']['stats']
