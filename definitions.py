class definitions:
    def __init__(self):
        return
    
    def get_teams(self):
        all_teams = {
        0: ['Free Agent', 'Free Agent', 'FA'],
        1: ['Atlanta','Hawks','ATL'],
        2: ['Boston', 'Celtics', 'BOS'],
        3: ['New Orleans','Pelicans','NOP'],
        4: ['Chicago', 'Bulls', 'CHI'],
        5: ['Cleveland', 'Cavaliers', 'CLE'],
        6: ['Dallas', 'Mavericks','DAL'],
        7: ['Denver', 'Nuggets', 'DEN'],
        8: ['Detroit' ,'Pistons','DET'],
        9: ['Golden State','Warriors','GS'],
        10: ['Houston','Rockets','HOU'],
        11: ['Indiana', 'Pacers','IND'],
        12: ['Los Angeles','Clippers','LAC'],
        13: ['Los Angeles','Lakers','LAL'],
        14: ['Miami','Heat','MIA'],
        15: ['Milwaukee','Bucks','MIL'],
        16: ['Minnesota','Timberwolves','MIN'],
        17: ['Brooklyn', 'Nets', 'BKN'],
        18: ['New York','Knicks','NYK'],
        19: ['Orlando','Magic','ORL'],
        20: ['Philadelphia','76ers','PHI'],
        21: ['Phoenix','Suns','PHX'],
        22: ['Portland','Trail Blazers','POR'],
        23: ['Sacramento','Kings','SAC'],
        24: ['San Antonio', 'Spurs', 'SA'],
        25: ['Oklahoma City','Thunder','OKC'],
        26: ['Utah','Jazz','UTA'],
        27: ['Washington','Wizards','WAS'],
        28: ['Toronto', 'Raptors','TOR'],
        29: ['Memphis','Grizzlies','MEM'],
        30: ['Charlotte', 'Hornets', 'CHA']
        }
        return all_teams
    def get_eligible_positions(self):
        eligible_positions = {
            1: 'PG',
            2: 'SG',
            3: 'SF',
            4: 'PF',
            5: 'C'
        }
        return eligible_positions
