# -*- coding: UTF-8 -*-
import copy
import statistics
import flask
import numpy as np
from flask import jsonify, request, json
from flask_cors import CORS

from player import player
from standard_deviation_container import standard_deviation_container
from team import team

from utils import read_json
from espn_fantasy_league import espn_fantasy_league
from definitions import definitions
from standard_deviation import standard_deviation

config = read_json("config.json")
cookies = config['cookies']
# cookies['espn_s2'].replace("%", "!");
league_settings = config['league']
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

# EspnFantasyLeague = espn_fantasy_league(cookies,league_settings)
# playerInfo = EspnFantasyLeague.get_players_data()
# statStandings = EspnFantasyLeague.make_stat_table()
# standings = EspnFantasyLeague.make_stat_standings_table()
# league_info = EspnFantasyLeague.get_division_team_setting_data()
# fantasy_team_data = EspnFantasyLeague.get_fantasy_teams_data()
# standings_info = EspnFantasyLeague.make_standings()
# definitions = definitions()

EspnFantasyLeague = None
playerInfo = None
statStandings = None
standings = None
league_info = None
fantasy_team_data = None
standings_info = None
definitions_obj = None
players_data = None
standard_deviation_cutoffs = None

@app.route('/generate-league', methods=['POST'])
def generate_league():
    global EspnFantasyLeague
    global playerInfo
    global statStandings
    global standings
    global league_info
    global fantasy_team_data
    global standings_info
    global definitions_obj
    global players_data
    global standard_deviation_cutoffs

    data = request.json  # Get data from the frontend

    # Update the configuration with data from the frontend
    config["cookies"]["swid"] = data["swid"]
    config["cookies"]["espn_s2"] = data["espn_s2"]
    config["league"]["league_id"] = int(data["league_id"])
    config["league"]["season"] = int(data["season"])

    # Optionally, you can save the updated configuration to a file if needed.
    # Create instances of objects after configuring cookies
    # Initialize the global variables here if they are not already initialized

    if data['swid'] is not None and data["swid"] is not None \
            and int(data["league_id"]) is not None and int(data["season"]) is not None:
        EspnFantasyLeague = espn_fantasy_league(config["cookies"], config["league"])
        playerInfo = EspnFantasyLeague.get_players_data()
        statStandings = EspnFantasyLeague.make_stat_table()
        standings = EspnFantasyLeague.make_stat_standings_table()
        league_info = EspnFantasyLeague.get_division_team_setting_data()
        fantasy_team_data = EspnFantasyLeague.get_fantasy_teams_data()
        standings_info = EspnFantasyLeague.make_standings()
        definitions_obj = definitions()
        # Generate Players for performance's sake
        players_data = generatePlayerInfo()
        standard_deviation_cutoffs = generateStandardDeviations();

    return jsonify({"message": "Configuration updated successfully"})

@app.route('/player-info', methods=['GET'])
def getPlayerInfoApi():
    return players_data

def generatePlayerInfo():
    players = copy.deepcopy(playerInfo['players'])
    all_teams = definitions_obj.get_teams()
    eligible_positions = definitions_obj.get_eligible_positions()
    for x in players:
        # Gives proper names to ratings
        if 'ratings' in x:
            if '0' in x['ratings']:
                x['ratings']['ratingsCurr'] = x['ratings'].pop('0')
            if '1' in x['ratings']:
                x['ratings']['ratingsPrev7'] = x['ratings'].pop('1')
            if '2' in x['ratings']:
                x['ratings']['ratingsPrev15'] = x['ratings'].pop('2')
            if '3' in x['ratings']:
                x['ratings']['ratingsPrev30'] = x['ratings'].pop('3')
        # Adds stat container object
        x['player']['statContainer'] = {}
        x['player']['statContainer']['currentSeason'] = x['player']['stats'][0]
        x['player']['statContainer']['lastFifteen'] = x['player']['stats'][1]
        x['player']['statContainer']['lastSeven'] = x['player']['stats'][2]
        if len(x['player']['stats']) > 3:
            x['player']['statContainer']['prevSeason'] = x['player']['stats'][3]
        if len(x['player']['stats']) > 4:
            x['player']['statContainer']['lastThirty'] = x['player']['stats'][4]
        if len(x['player']['stats']) > 5:
            x['player']['statContainer']['seasonProjections'] = x['player']['stats'][5]
        if len(x['player']['stats']) == 7:
            x['player']['statContainer']['prevSeasonProjections'] = x['player']['stats'][6]
        curr_team_id = x['player']['proTeamId']
        team_name = all_teams[curr_team_id][2]
        x['player']['proTeamId'] = team_name
        curr_position = x['player']['defaultPositionId']
        position = eligible_positions[curr_position]
        x['player']['defaultPositionId'] = position
    return players


@app.route('/standard-deviations', methods=['GET'])
def getStandardDeviations():
    return jsonify(standard_deviation_cutoffs)

# WORKS
def generateStandardDeviations():
    players = copy.deepcopy(playerInfo['players'])
    #standardDeviations = generateStandardDeviations(players)
    standardDeviations = standard_deviation()
    for x in players:
        index = 0;
        stats = x['player']['stats']
        # print(x['player']['fullName'])
        for period in stats:
            # print(period)
            map_standard_deviations(standardDeviations, period, index)
            index = index + 1;

    standard_deviations_Dict = standardDeviations.to_dict()
    #standard_deviations_data = standardDeviations.to_dict()
    temp_dict = {}
    for key, value in standard_deviations_Dict.items():
        cutoffs = calculate_standard_deviations(value, key)
        temp_dict[key] = cutoffs

    return temp_dict

#WORKS
@app.route('/player-rankings', methods=['GET'])
def getPlayerRankings():
    players = playerInfo['players']
    player_list = []
    for x in players:
        player_list.append(x['player'])
    all_teams = definitions_obj.get_teams()
    eligible_positions = definitions_obj.get_eligible_positions()
    player_list = map_teams(player_list, all_teams)
    player_list = map_eligible_positions(player_list, eligible_positions)
    return player_list

# WORKS
@app.route('/fantasy-stat-titles', methods=['GET'])
def getFantasyStatTitles():
    return EspnFantasyLeague.fantasy_stats

# WORKS
@app.route('/league', methods=['GET'])
def getLeagueInfo():
    fantasy_teams = fantasy_team_data['teams']
    teams_list = []
    for fantasy_team in fantasy_teams:
        x = team(fantasy_team)
        team_json = json.dumps(dict(x), default=lambda obj: obj.__dict__)
        teams_list.append(team_json)
    return jsonify(teams_list)

# WORKS
@app.route('/rosters', methods=['GET'])
def getRosters():
    fantasy_teams = fantasy_team_data['teams']
    rosters = []
    for fantasy_team in fantasy_teams:
        roster_entries = fantasy_team['roster']['entries']
        players = []
        for entry in roster_entries:
            x = player(entry)
            player_json = json.dumps(x, default=lambda obj:
            obj.__dict__)
            players.append(player_json)
        rosters.append(players)
    return jsonify(rosters)

@app.route('/', methods=['GET'])
def root():
    return 'Hello world'

def map_standard_deviations(standardDeviations, period, index):
    # Average Stats
    if 'averageStats' in period.keys():
        average_stats = period['averageStats']
        if index == 0:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_curr.append(average_stats['0'])

            if '1' in average_stats.keys():
                standardDeviations.blocks_avg_curr.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_curr.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_curr.append(average_stats['3'])
            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_curr.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_curr.append(average_stats['11'])
            if '14' in average_stats.keys():
                standardDeviations.fga_avg_curr.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_curr.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_curr.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_curr.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_curr.append(average_stats['15'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_curr.append(average_stats['17'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_curr.append(average_stats['20'])
        if index == 1:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_15.append(average_stats['0'])
            if '1' in average_stats.keys():

                standardDeviations.blocks_avg_15.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_15.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_15.append(average_stats['3'])
            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_15.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_15.append(average_stats['11'])
            if '14' in average_stats.keys():
                standardDeviations.fga_avg_15.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_15.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_15.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_15.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_15.append(average_stats['15'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_15.append(average_stats['20'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_15.append(average_stats['17'])
        if index == 2:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_7.append(average_stats['0'])
            if '1' in average_stats.keys():
                standardDeviations.blocks_avg_7.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_7.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_7.append(average_stats['3'])
            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_7.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_7.append(average_stats['11'])
            if '14' in average_stats.keys():
                standardDeviations.fga_avg_7.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_7.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_7.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_7.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_7.append(average_stats['15'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_7.append(average_stats['17'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_7.append(average_stats['20'])
        if index == 3:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_prev.append(average_stats['0'])
            if '1' in average_stats.keys():
                standardDeviations.blocks_avg_prev.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_prev.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_prev.append(average_stats['3'])

            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_prev.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_prev.append(average_stats['11'])
            if '14' in average_stats.keys():
                standardDeviations.fga_avg_prev.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_prev.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_prev.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_prev.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_prev.append(average_stats['15'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_prev.append(average_stats['17'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_prev.append(average_stats['20'])
        if index == 4:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_30.append(average_stats['0'])
            if '1' in average_stats.keys():
                standardDeviations.blocks_avg_30.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_30.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_30.append(average_stats['3'])
            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_30.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_30.append(average_stats['11'])
            if '14' in average_stats.keys():
                standardDeviations.fga_avg_30.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_30.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_30.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_30.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_30.append(average_stats['15'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_30.append(average_stats['17'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_30.append(average_stats['20'])
        if index == 5:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_proj.append(average_stats['0'])
            if '1' in average_stats.keys():
                standardDeviations.blocks_avg_proj.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_proj.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_proj.append(average_stats['3'])
            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_proj.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_proj.append(average_stats['11'])
            if '14' in average_stats.keys():

                standardDeviations.fga_avg_proj.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_proj.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_proj.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_proj.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_proj.append(average_stats['15'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_proj.append(average_stats['17'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_proj.append(average_stats['20'])
        if index == 6:
            if '0' in average_stats.keys():
                standardDeviations.points_avg_prevProj.append(average_stats['0'])
            if '1' in average_stats.keys():
                standardDeviations.blocks_avg_prevProj.append(average_stats['1'])
            if '2' in average_stats.keys():
                standardDeviations.steals_avg_prevProj.append(average_stats['2'])
            if '3' in average_stats.keys():
                standardDeviations.assists_avg_prevProj.append(average_stats['3'])
            if '6' in average_stats.keys():
                standardDeviations.rebounds_avg_prevProj.append(average_stats['6'])
            if '11' in average_stats.keys():
                standardDeviations.turnovers_avg_prevProj.append(average_stats['11'])
            if '14' in average_stats.keys():
                standardDeviations.fga_avg_prevProj.append(average_stats['14'])
            if '13' in average_stats.keys():
                standardDeviations.fgm_avg_prevProj.append(average_stats['13'])
            if '19' in average_stats.keys():
                standardDeviations.fgp_avg_prevProj.append(average_stats['19'])
            if '16' in average_stats.keys():
                standardDeviations.fta_avg_prevProj.append(average_stats['16'])
            if '15' in average_stats.keys():
                standardDeviations.ftm_avg_prevProj.append(average_stats['15'])
            if '17' in average_stats.keys():
                standardDeviations.tpm_avg_prevProj.append(average_stats['17'])
            if '20' in average_stats.keys():
                standardDeviations.ftp_avg_prevProj.append(average_stats['20'])
    # Total Stats
    if 'stats' in period.keys():
        totals = period['stats']
        if index == 0:
            if '0' in totals.keys():
                standardDeviations.points_curr.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_curr.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_curr.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_curr.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_curr.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_curr.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_curr.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_curr.append(totals['13'])

            if '19' in totals.keys():
                standardDeviations.fgp_curr.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_curr.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_curr.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_curr.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_curr.append(totals['20'])
        if index == 1:
            if '0' in totals.keys():
                standardDeviations.points_15.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_15.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_15.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_15.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_15.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_15.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_15.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_15.append(totals['13'])
            if '19' in totals.keys():
                standardDeviations.fgp_15.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_15.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_15.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_15.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_15.append(totals['20'])
        if index == 2:
            if '0' in totals.keys():
                standardDeviations.points_7.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_7.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_7.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_7.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_7.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_7.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_7.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_7.append(totals['13'])
            if '19' in totals.keys():
                standardDeviations.fgp_7.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_7.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_7.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_7.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_7.append(totals['20'])
        if index == 3:
            if '0' in totals.keys():
                standardDeviations.points_prev.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_prev.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_prev.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_prev.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_prev.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_prev.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_prev.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_prev.append(totals['13'])
            if '19' in totals.keys():
                standardDeviations.fgp_prev.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_prev.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_prev.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_prev.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_prev.append(totals['20'])
        if index == 4:
            if '0' in totals.keys():
                standardDeviations.points_30.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_30.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_30.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_30.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_30.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_30.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_30.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_30.append(totals['13'])
            if '19' in totals.keys():
                standardDeviations.fgp_30.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_30.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_30.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_30.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_30.append(totals['20'])
        if index == 5:
            if '0' in totals.keys():
                standardDeviations.points_proj.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_proj.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_proj.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_proj.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_proj.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_proj.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_proj.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_proj.append(totals['13'])
            if '19' in totals.keys():
                standardDeviations.fgp_proj.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_proj.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_proj.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_proj.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_proj.append(totals['20'])
        if index == 6:
            if '0' in totals.keys():
                standardDeviations.points_prevProj.append(totals['0'])
            if '1' in totals.keys():
                standardDeviations.blocks_prevProj.append(totals['1'])
            if '2' in totals.keys():
                standardDeviations.steals_prevProj.append(totals['2'])
            if '3' in totals.keys():
                standardDeviations.assists_prevProj.append(totals['3'])
            if '6' in totals.keys():
                standardDeviations.rebounds_prevProj.append(totals['6'])
            if '11' in totals.keys():
                standardDeviations.turnovers_prevProj.append(totals['11'])
            if '14' in totals.keys():
                standardDeviations.fga_prevProj.append(totals['14'])
            if '13' in totals.keys():
                standardDeviations.fgm_prevProj.append(totals['13'])
            if '19' in totals.keys():
                standardDeviations.fgp_prevProj.append(totals['19'])
            if '16' in totals.keys():
                standardDeviations.fta_prevProj.append(totals['16'])
            if '15' in totals.keys():
                standardDeviations.ftm_prevProj.append(totals['15'])
            if '17' in totals.keys():
                standardDeviations.tpm_prevProj.append(totals['17'])
            if '20' in totals.keys():
                standardDeviations.ftp_prevProj.append(totals['20'])
def map_teams(player_list, all_teams):
    player_list_copy = copy.deepcopy(player_list)
    for player in player_list_copy:
        curr_team_id = player['proTeamId']
        team_name = all_teams[curr_team_id][1]
        player['proTeamId'] = team_name
    return player_list_copy
def map_eligible_positions(player_list, eligible_positions):
    player_list_copy = copy.deepcopy(player_list)
    for player in player_list_copy:
        curr_position = player['defaultPositionId']
        position = eligible_positions[curr_position]
        player['defaultPositionId'] = position
    return player_list_copy

def calculate_standard_deviations(arr, key):
    if not arr:
        return []
    # Convert the input list to a NumPy array
    data_array = np.array(arr)

    if 'ftp' in key or 'fgp' in key:
        # Take out non-qualifying data such as 0 or 1.0 (100%)
        filtered_data = [x for x in data_array if x != 0.0 and x != 1.0]
        # Calculate the mean and standard deviation of the data
        mean = np.mean(filtered_data)
        std_dev = np.std(filtered_data) / 2

        # Calculate the cutoff points for -3, -2, -1, 0, 1, 2, and 3 standard deviations from the mean
        cutoff_points = [
            # mean - 3 * std_dev,
            max(mean - 2 * std_dev, 0),
            max(mean - std_dev, 0),
            mean,
            mean + std_dev,
            mean + 2 * std_dev,
            mean + 3 * std_dev
        ]
        return cutoff_points

    else:
        # Take out non-qualifying data such as 0 or 1.0 (100%)
        filtered_data = [x for x in data_array if x != 0 and x != 0.0]

        # Calculate the mean and standard deviation of the data
        mean = np.mean(filtered_data)
        std_dev = np.std(filtered_data)

        # Calculate the cutoff points for -3, -2, -1, 0, 1, 2, and 3 standard deviations from the mean
        cutoff_points = [
            #mean - 3 * std_dev,
            max(mean - 2 * std_dev, 0),
            max(mean - std_dev, 0),
            mean,
            mean + std_dev,
            mean + 2 * std_dev,
            mean + 3 * std_dev
        ]

        return cutoff_points

app.run()
