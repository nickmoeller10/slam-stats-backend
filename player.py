class player:
    def __init__(self, entry):
        self.player_id = entry['playerPoolEntry']['player']['id']
        self.name = entry['playerPoolEntry']['player']['fullName']
        self.team = entry['playerPoolEntry']['player']['proTeamId']
        self.on_team_id = entry['playerPoolEntry']['onTeamId']
        self.position = entry['playerPoolEntry']['player']['defaultPositionId']
        self.injury_status = entry['playerPoolEntry']['player']['injuryStatus']
        self.stats = entry['playerPoolEntry']['player']['stats']
        self.ratings = entry['playerPoolEntry']['ratings']
        self.eligible_positions = entry['playerPoolEntry']['player']['eligibleSlots']
        self.keeper_curr_val = entry['playerPoolEntry']['keeperValue']
        self.keeper_future_val = entry['playerPoolEntry']['keeperValueFuture']
        self.team_status = entry['playerPoolEntry']['status']
        self.acquisition_type = entry['acquisitionType']
        self.average_draft_position = entry['playerPoolEntry']['player']['ownership']['averageDraftPosition']
        self.percent_owned = entry['playerPoolEntry']['player']['ownership']['percentOwned']
        self.percent_started = entry['playerPoolEntry']['player']['ownership']['percentStarted']

