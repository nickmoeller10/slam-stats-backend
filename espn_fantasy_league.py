import requests
import json
import numpy as np
import pandas as pd
from utils import (
    advanced_stats_by_fantasy_team,
    matchup_stats
)
from utils import get_logger
logger = get_logger(__name__)

class espn_fantasy_league:
    """
    Class for data collection
    """
    def __init__(self, cookies, league_settings):
        self.dtypes = {'FG%': float, 'FT%': float, '3PM': int, 'REB': int,
        'AST': int, 'STL': int, 'BLK': int, 'TO': int,
        'PTS': int, 'FTA': int, 'FTM': int,
        'FGA': int, 'FGM': int}
        self.stat_id_abbr_dict = {'0': 'PTS', '1': 'BLK', '2': 'STL',
        '3': 'AST', '6': 'REB', '11': 'TO',
        '13': 'FGM', '14': 'FGA',
        '15': 'FTM', '16': 'FTA',
        '17': '3PM',
        '19': 'FG%', '20': 'FT%'}
        self.adv_stats_dict = {'40': 'Mins', '42': 'Games'}
        self.fantasy_stats = ['FG%', 'FT%', '3PM', 'REB',
        'AST', 'STL', 'BLK', 'TO', 'PTS']
        # stats needed for simulation
        self.stats_aux = ['FGM', 'FGA', 'FTM', 'FTA', 'FG%', 'FT%',
        '3PM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
        # stats simulated with a poisson distribution
        self.poisson_stats = ['FGA', 'FTA', '3PM', 'REB', 'AST',

        'STL', 'BLK', 'TO', 'PTS']
        self.simulation_stats = self.poisson_stats + ['FGM', 'FTM']
        self.team_id_abbr_dict = {}
        self.team_id_name_dict = {}
        self.team_abbr_name_dict = {}
        self.division_id_name_dict = {}
        self.n_teams = None
        self.division_setting_data = None
        self.fantasy_teams_data = None
        self.league_id = league_settings["league_id"]
        self.season = league_settings["season"]
        self.cookies = cookies
        url_fantasy_league = (
        "http://fantasy.espn.com/apis/v3/games/fba/seasons/{}/"
        + "segments/0/leagues/{}"
        )
        url_nba = "http://fantasy.espn.com/apis/v3/games/fba/seasons/{}"
        self.url_fantasy = url_fantasy_league.format(
        self.season, self.league_id)
        self.url_nba = url_nba.format(self.season)
        self.set_league_team_division_settings()
        return
    def get_espn_data(self, url_endpoint, endpoints=[], headers=None,
    **kargs):
        '''
        Fetch data from the ESPN:
        For fantasy league data the available end-points are:
        * mDraftDetail
        * mLiveScoring
        * mMatchup
        * mPendingTransactions
        * mPositionalRatings
        * mSettings
        * mTeam
        * modular
        * mNav
        * mMatchupScore
        * mStandings
        * mRoster
        * mBoxscore
        * kona_player_info
        * player_wl
        For NBA teams data the available end-point is:
        * proTeamSchedules
        '''
        params = {'view': endpoints, **kargs}
        r = requests.get(url_endpoint, cookies=self.cookies, params=params,
        headers=headers)

        if r.status_code != 200:
            raise ValueError('Error fetching the teams data')
        data = r.json()
        return data
    
    def get_division_team_setting_data(self):
        '''
        Fetch division teams' basic data and settings; ids, logos, names,
        owners, abbreviations, etc.
        '''
        if self.division_setting_data is None:
            self.division_setting_data = self.get_espn_data(
                self.url_fantasy, endpoints=['mTeam', 'mSettings']
        )
        return self.division_setting_data
    
    def get_fantasy_teams_data(self):
        '''
        Fetch fantasy teams' data; schedule, roster, etc.
        '''
        if self.fantasy_teams_data is None:
            self.fantasy_teams_data = self.get_espn_data(
                self.url_fantasy,
                endpoints=['mTeam', 'mSettings', 'mMatchup', "mRoster"]
        )
        return self.fantasy_teams_data
    
    def get_players_data(self):
        '''
        '''
        filters = {
            "players": {
            # "filterStatus": {
            # "value": ["FREEAGENT", "WAIVERS"]
            # },
            "limit": 5000,
            "sortDraftRanks": {
                "sortPriority": 100,
                "sortAsc": True,
                "value": "STANDARD"
                }
            }
        }
        headers = {'x-fantasy-filter': json.dumps(filters)}
        data = self.get_espn_data(
            self.url_fantasy,
            endpoints=['kona_player_info'],
            headers=headers
        )
        return data
    def set_league_team_division_settings(self):
        '''
        Requires `mTeam` and `mSettings` endpoints
        '''
        data = self.get_division_team_setting_data()
    
        self.team_id_abbr_dict = {
            team['id']: team['abbrev'] for team in data['teams']
        }
        self.team_id_name_dict = {
            team['id']: team['location'] + ' ' + team['nickname']
            for team in data['teams']
        }
        self.team_abbr_name_dict = {
            v: self.team_id_name_dict[k]
            for k, v in self.team_id_abbr_dict.items()
        }
        self.division_id_name_dict = {
            u['id']: u['name']
            for u in data['settings']['scheduleSettings']['divisions']
        }
        if len(self.division_id_name_dict) > 1:
            logger.warning('There are more than 1 divisions')
        self.n_teams = len(data['teams'])
        logger.info('%d teams participating' % self.n_teams)
        lineupslots = data['settings']['rosterSettings']['lineupSlotCounts']
        # 0 to 11 are valid roster slots. slot 12 is bench, slot 13 is IR.
        self.n_starters = sum(
            [v for k, v in lineupslots.items() if int(k) < 12]
        )
        logger.info('%d starters per team' % self.n_starters)
        return
    def make_stat_table(self):
        '''
        Makes the *current* total stat table of the fantasy league teams
        It requires the `mTeam` endpoint data
        '''
        data = self.get_division_team_setting_data()

      #  stats = [team['valuesByStat'] for team in data['teams']]
        if all('valuesByStat' in team for team in data['teams']):
            stats = [team['valuesByStat'] if 'valuesByStat' in team else None for team in data['teams']]
            team_abbrs = [team['abbrev'] for team in data['teams']]
            # make dataframe
            stat_table = pd.DataFrame(data=stats, index=team_abbrs)
            # select only headers of interest
            stat_table = stat_table.loc[:, self.stat_id_abbr_dict.keys()]
            # rename stat headers to match the web app
            stat_table.rename(columns=self.stat_id_abbr_dict, inplace=True)
            # update the column data types
            stat_table.astype(self.dtypes)
            return stat_table[self.fantasy_stats]
        else:
            # Need to fix this.
            team_abbrs = [team['abbrev'] for team in data['teams']]
            default_data = pd.DataFrame(0, index=team_abbrs, columns=self.fantasy_stats)
            # stats = [team['valuesByStat'] if 'valuesByStat' in team else None for team in data['teams']]
            # stat_table = pd.DataFrame(data=stats, index=team_abbrs)
            return default_data
    def make_standings(self, division='all'):
        '''
        Makes the *current* standings table of the fantasy teams
        It requires the `mTeam` and `mSettings` endpoint data
        '''
        data = self.get_division_team_setting_data()
        if len(self.division_id_name_dict) == 0:
            self.division_id_name_dict = {
            u['id']: u['name'] for u in
            data['settings']['scheduleSettings']['divisions']
            }

        team_abbrs = [team['abbrev'] for team in data['teams']]
        division_ids = [self.division_id_name_dict[team['divisionId']]
                        for team in data['teams']]
        record = [team['record']['overall'] for team in data['teams']]
        standings = pd.DataFrame(data=record, index=team_abbrs)
        standings = standings.loc[:, ['wins', 'losses', 'ties',
        'percentage']]
        standings['Division'] = division_ids
        if len(self.division_id_name_dict) > 1:
            if division.lower() == 'west':
                standings = standings[standings['Division'] == 'West']
            elif division.lower() == 'east':
                standings = standings[standings['Division'] == 'East']
        standings = standings.sort_values('percentage', ascending=False)
        standings['Rank'] = np.arange(1, standings.shape[0] + 1, dtype=int)
        return standings

    def make_stat_standings_table(self):
        '''
        Merges the stat and standings table of the fantasy teams
        '''
        # make the stat table
        stat_table = self.make_stat_table()
        # make the standings table
        standings = self.make_standings()
        # merge the two on the indices
        table = standings.merge(stat_table, right_index=True,
        left_index=True)
        return table

    def get_fantasy_team_stats_per_round(self):
        '''
        Get the total statistics for each fantasy team and each round/week.
        It requires `mTeam`, `mRoster`, `mSettings`, `mMatchup`
        '''
        data = self.get_fantasy_teams_data()
        stat_cols = sorted(self.stat_id_abbr_dict.keys())
        datastore = []
        for i, match in enumerate(data['schedule']):
            if ('home' in match) and ('away' in match):
                tmp_home = matchup_stats(match, stat_cols, 'home')
                tmp_away = matchup_stats(match, stat_cols, 'away')
                if tmp_home is None or tmp_away is None:
                    break
                datastore.append(tmp_home)
                datastore.append(tmp_away)
            else:
                logger.warning('Warning, match not found')
        headers = ['Round', 'teamId', 'where', 'wins', 'losses', 'ties']
        cols = headers + stat_cols
        df = pd.DataFrame(datastore, columns=cols)

        df.rename(columns=self.stat_id_abbr_dict, inplace=True)
        df['teamId'] = df['teamId'].replace(self.team_id_abbr_dict)
        df.rename(columns={'teamId': 'teamAbbr'}, inplace=True)
        df.set_index('teamAbbr', inplace=True)
        return df

    def get_total_team_stats_upto_round(self, week):
        '''
        Get the total statistics for each fantasy team from the beginning of
        season up to a specified week. If wee = current week, this function
        is equivalent to the `make_stat_table` method above.
        It requires `mTeam`, `mRoster`, `mSettings`, `mMatchup`
        '''
        table = self.get_fantasy_team_stats_per_round()
        table = table[table['Round'] <= week]
        stats = list(self.stat_id_abbr_dict.values())
        aggregate = table.groupby('teamAbbr')[stats].sum()
        aggregate['FT%'] = aggregate['FTM'] / aggregate['FTA']
        aggregate['FG%'] = aggregate['FGM'] / aggregate['FGA']
        return aggregate[self.fantasy_stats]

    def get_adv_stats_per_fantasy_team(self, week, scoring_period=None):
        '''
        Get the total minutes and games played for all teams in the leaguge
        for
        a given week/round.
        `scoring_period` is optional, if provided, it simply makes the data
        extraction faster.
        '''
        if scoring_period is None:
            # If `scoring_period` is None, loop over all scoring periods to
            # find
            # the one that matches with the given week/round.
            # Loop in reverse order, because we often query the latest
            # matchup/week. Don't need to loop in increments of 1, as long as
            # the scoring period within the given week/round it will return
            # the
            # right result (tested!). Increments of 3 should suffice.
            range_ = range(self.division_setting_data["scoringPeriodId"], 0, -3)
        else:
            # If `scoring_period` is given "scan" only the given period, here
            # we create an "iterable" of a single element for
            # generalisability.
            range_ = range(scoring_period, scoring_period + 1)
        found = False
        for scoring_period in range_:
            if not found:
                data = self.get_espn_data(
                self.url_fantasy,
                endpoints=['mMatchup', 'mMatchupScore'],
                scoringPeriodId=scoring_period
                )
            else:

                break
            data_list = []
            matchupPeriodId = []
            stat_codes = list(self.adv_stats_dict.keys())
            for matchup in data['schedule']:
                if ((matchup['matchupPeriodId'] == week)
                    and ('rosterForMatchupPeriod' in matchup['home'])
                    and ('rosterForMatchupPeriod' in matchup['away'])):
                    found = True
                    matchupPeriodId.append(matchup['matchupPeriodId'])
                    home_abbr = self.team_id_abbr_dict[
                        matchup['home']['teamId']]
                    away_abbr = self.team_id_abbr_dict[
                        matchup['away']['teamId']]
                    home_stats = advanced_stats_by_fantasy_team(
                        matchup['home'],
                        stat_codes
                    )
                    away_stats = advanced_stats_by_fantasy_team(
                    matchup['away'],
                    stat_codes
                    )
                    df = pd.concat((home_stats, away_stats), axis=1)
                    df.rename(
                        columns={0: home_abbr, 1: away_abbr},
                        inplace=True
                    )
                    data_list.append(df)
        if not matchupPeriodId:
            err_msg = (
            f"Scoring period {scoring_period} does not "
            + f"correspond to input round {week}"
            )
            logger.error(err_msg)
            raise ValueError(err_msg)
        data_df = pd.concat(data_list, axis=1)
        data_df = data_df.T.rename(columns=self.adv_stats_dict)
        return data_df
