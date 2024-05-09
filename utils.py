import pandas as pd
import os
import ast
from collections import defaultdict
from data_processing import *
import re
from bs4 import BeautifulSoup, Comment
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.manifold import TSNE
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

# Set general constant
matplotlib.use('TkAgg')
SIDE = {'Total' : 0, 'Side 1' : 1, 'Side 2' : 2}
NAME = ['logaN', 'Wailers', 'beyAz', 'TakaS', 'nataNk']
TEAM = "Gentle Mates"

#region BasicStatistiques

def calculate_action_player(name, data, average, action, side):
    """
    Functions that calculate the number of action by side

    parameter:
        name : name of the player | string
        data : dataframe of the retrieve data from the scraper
        average : boolean if true then calculate the average, sum otherwise
        action : either 'K' or 'D'
        side : ATK, DFS or full match
    
    return:
        report : a dictionnary with the name as key and the calculated value
    """
    report = {name: 0}
    actions = []

    side_mapping = {'Total': 0, 'Side 1': 1, 'Side 2': 2}
    side_ = side_mapping.get(side, None)
    
    if side_ is None:
        side_ = 0
    
    action_ = action if action in ['K', 'D'] else 'K'
    
    for i, _ in enumerate(data):
        actions.append(int(data[action_].iloc[i].split('\n')[side_]))
    
    if average:
        report[name] = calculate_average(actions)
    else:
        report[name] = sum(actions)
    
    return report

def calculate_action_team(names, data, average, action, side):
    """
    Functions that calculate the number of action by side by player for the all team

    parameter:
        names : names of the player of the team | list of string
        data : dataframe of the retrieve data from the scraper
        average : boolean if true then calculate the average, sum otherwise
        action : either 'K' or 'D'
        side : ATK, DFS or full match
    
    return:
        report : a dictionnary with the names as keys and the calculated value for each name
    """
    report = {n: [] for n in names}
    
    side_mapping = {'Total': 0, 'Side 1': 1, 'Side 2': 2}
    side_ = side_mapping.get(side, None)
    
    if side_ is None:
        side_ = 0
    
    action_ = action if action in ['K', 'D'] else 'K'
    
    for i, _ in enumerate(data):
        name = data.iloc[i]['Player Name']
        report[name].append(int(data[action_].iloc[i].split('\n')[side_]))
    
    if average:
        final_report = {n: calculate_average(report[n]) for n in names}
    else:
        final_report = {n: sum(report[n]) for n in names}
    
    return final_report

def calculate_score_player(data,name, type, side):

    report = {name: 0}
    scores = []

    side_mapping = {'Total': 0, 'Side 1': 1, 'Side 2': 2}
    side_ = side_mapping.get(side, None)
    
    if side_ is None:
        side_ = 0
    
    for i,_ in enumerate(data):
        scores.append(int(data[type].iloc[i].split('\n')[side_]))
    return 0
 
def calculate_score_team():
    return 0

@st.cache_data
def calculate_average_rating_players(df, side = None):
    """ 
    Function that calculate the average rating of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    index_side = 0
    if side is not None:
        if side == 'ATK':
            index_side = 1
        elif side == 'DFS':
            index_side = 2
        else:
            print('Side is either None, ATK or DFS')

    average_rating_scores = {player : ( list(set(df[df['Player Name'] == player].dropna()['Team Name']))[0],round(sum(df[df['Player Name'] == player].dropna()['R'].apply(lambda x: float(x.split('\n')[index_side]))) / len(df[df['Player Name'] == player].dropna()), 2)) for player in list(set(df['Player Name']))}
    # Convert dictionary to DataFrame
    df_rating = pd.DataFrame.from_dict(average_rating_scores, orient='index', columns=['team', 'rating']).reset_index()
    # Rename index column to 'player'
    df_rating.rename(columns={'index': 'player'}, inplace=True)
    return df_rating

@st.cache_data
def calculate_average_kills_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """    
    index_side = 0
    if side is not None:
        if side == 'ATK':
            index_side = 1
        elif side == 'DFS':
            index_side = 2
        else:
            print('Side is either None, ATK or DFS')

    average_kills = {player : ( list(set(df[df['Player Name'] == player].dropna()['Team Name']))[0],round(sum(df[df['Player Name'] == player].dropna()['K'].apply(lambda x: float(x.split('\n')[index_side]))) / len(df[df['Player Name'] == player].dropna()), 2)) for player in list(set(df['Player Name']))}
    # Convert dictionary to DataFrame
    df_kills = pd.DataFrame.from_dict(average_kills, orient='index', columns=['team', 'kills']).reset_index()
    # Rename index column to 'player'
    df_kills.rename(columns={'index': 'player'}, inplace=True)
    return df_kills

def calculate_average_death_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    index_side = 0
    if side is not None:
        if side == 'ATK':
            index_side = 1
        elif side == 'DFS':
            index_side = 2
        else:
            print('Side is either None, ATK or DFS')

    average_deaths = {player : ( list(set(df[df['Player Name'] == player].dropna()['Team Name']))[0],round(sum(df[df['Player Name'] == player].dropna()['D'].apply(lambda x: float(x.strip().split('\n')[index_side]))) / len(df[df['Player Name'] == player].dropna()), 2)) for player in list(set(df['Player Name']))}
    # Convert dictionary to DataFrame
    df_deaths = pd.DataFrame.from_dict(average_deaths, orient='index', columns=['team', 'deaths']).reset_index()
    # Rename index column to 'player'
    df_deaths.rename(columns={'index': 'player'}, inplace=True)
    return df_deaths

@st.cache_data
def calculate_average_adr_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    index_side = 0

    if side is not None:
        if side == 'ATK':
            index_side = 1
        elif side == 'DFS':
            index_side = 2
        else:
            print('Side is either None, ATK or DFS')

    average_adr = {player : ( list(set(df[df['Player Name'] == player].dropna()['Team Name']))[0],round(sum(df[df['Player Name'] == player].dropna()['ADR'].apply(lambda x: float(x.split('\n')[index_side]))) / len(df[df['Player Name'] == player].dropna()), 2)) for player in list(set(df['Player Name']))}
    # Convert dictionary to DataFrame
    df_adr = pd.DataFrame.from_dict(average_adr, orient='index', columns=['team', 'adr']).reset_index()
    # Rename index column to 'player'
    df_adr.rename(columns={'index': 'player'}, inplace=True)

    return df_adr

@st.cache_data
def calculate_average_hs_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    
    index_side = 0

    if side is not None:
        if side == 'ATK':
            index_side = 1
        elif side == 'DFS':
            index_side = 2
        else:
            print('Side is either None, ATK or DFS')

    average_hs = {player : ( list(set(df[df['Player Name'] == player].dropna()['Team Name']))[0],round(sum(df[df['Player Name'] == player].dropna()['HS%'].apply(lambda x: float(x.split('\n')[index_side][:-1]))) / len(df[df['Player Name'] == player].dropna()), 2)) for player in list(set(df['Player Name']))}
    # Convert dictionary to DataFrame
    df_hs = pd.DataFrame.from_dict(average_hs, orient='index', columns=['team', 'hs']).reset_index()
    # Rename index column to 'player'
    df_hs.rename(columns={'index': 'player'}, inplace=True)

    return df_hs

@st.cache_data
def calculate_average_fk_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    index_side = 0

    if side is not None:
        if side == 'ATK':
            index_side = 1
        elif side == 'DFS':
            index_side = 2
        else:
            print('Side is either None, ATK or DFS')

    average_fk = {player : ( list(set(df[df['Player Name'] == player].dropna()['Team Name']))[0],round(sum(df[df['Player Name'] == player].dropna()['FK'].apply(lambda x: float(x.split('\n')[index_side]))) / len(df[df['Player Name'] == player].dropna()), 2)) for player in list(set(df['Player Name']))}
    # Convert dictionary to DataFrame
    df_fk = pd.DataFrame.from_dict(average_fk, orient='index', columns=['team', 'fk']).reset_index()
    # Rename index column to 'player'
    df_fk.rename(columns={'index': 'player'}, inplace=True)

    return df_fk

def calculate_average_fd_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_fd = {player : round(sum(df[df['Player Name'] == player].dropna()['FK/FD +/–'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_fd
    elif side == 'ATK':
        average_fd = {player : round(sum(df[df['Player Name'] == player].dropna()['FK/FD +/–'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_fd
    elif side == 'DFS':
        average_fd = {player : round(sum(df[df['Player Name'] == player].dropna()['FK/FD +/–'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_fd
    else:
        print(f'Side is either None, ATK or DFS')

def filter_by_scope(data, scope):
    """
    Function that keep only the wanted match, get the all tournament by default

    parameter:
        data : dataframe of the retrieve data from the scraper
        scope : string representing the instance that is under study i.e the match or the all tournament
    """
    if scope:
        try:
            data = data[data["Series"] == scope]
            return data
        except KeyError:
            print(f'Side {scope} is not specified so returning all data.')
            return data
    else:
        return data

def calculate_average(lst):
    return sum(lst) / len(lst)

def number_action_by_player_by_scope(df, action, average, side=None, scope=None, name=None, team_name=None):
    """
    Functions that calculate the number of action by side by player and by scope

    parameter:
        df : dataframe of the retrieve data from the scraper
        average : boolean if true then calculate the average, sum otherwise
        scope : string representing the instance that is under study i.e the match or the all tournament set to None by default
        name : name of the player | string
        action : either 'K' or 'D'
        side : ATK, DFS or full match set to None by default
        team_name : name of the teamp that is under study | string
    
    return:
        report : a dictionnary with the names as keys and the calculated value for each name
    """
    if name is not None:
        try:
            data_player = df[df['Player Name'] == name]
        except NameError:
            print(f'No such {name} in the dataset : {NameError}')
        data_player_filtered_by_scope = filter_by_scope(data_player, scope)
        report_player = calculate_action_player(name, data_player_filtered_by_scope, average, action, side)

        return report_player

    elif team_name is not None:
        try:
            set_names = set(df['Player Name'].where(df['Team Name'] == team_name))
        except NameError:
            print(f'No such {set_names} in the dataset : {NameError}')

        names = pd.DataFrame(list(set_names), columns=['Player']).dropna()['Player'].values.tolist()
        data_team = df[df['Player Name'].isin(names)]
        data_team_filtered_by_scope = filter_by_scope(data_team, scope)
        report_team = calculate_action_team(names, data_team_filtered_by_scope, average, action, side)

        return report_team
    else:
        raise ValueError('No instance can be treated')
    
def average_score_by_player_by_scope(df, type, side=None, scope=None, name=None, team_name=None):
    """
    Functions that calculate the average score by side by player and by scope

    parameter:
        df : dataframe of the retrieve data from the scraper
        type : type of the score wanted | 'ACS' or 'ADR'
        scope : string representing the instance that is under study i.e the match or the all tournament set to None by default
        name : name of the player | string
        action : either 'K' or 'D'
        side : ATK, DFS or full match set to None by default
        team_name : name of the teamp that is under study | string
    
    return:
        report : a dictionnary with the names as keys and the calculated value for each name
    """
    if name is not None:
        try:
            data_player = df[df['Player Name'] == name]
        except NameError:
            print(f'No such {name} in the dataset : {NameError}')
        data_player_filtered_by_scope = filter_by_scope(data_player, scope)
        report_player = calculate_score_player(name, data_player_filtered_by_scope, type, side)

        return report_player

    elif team_name is not None:
        try:
            set_names = set(df['Player Name'].where(df['Team Name'] == team_name))
        except NameError:
            print(f'No such {set_names} in the dataset : {NameError}')

        names = pd.DataFrame(list(set_names), columns=['Player']).dropna()['Player'].values.tolist()
        data_team = df[df['Player Name'].isin(names)]
        data_team_filtered_by_scope = filter_by_scope(data_team, scope)
        report_team = calculate_score_team(names, data_team_filtered_by_scope, type, side)

        return report_team
    else:
        raise ValueError('No instance can be treated')

def set_map_winner(df):
    """
    Function that create a column for the map winner based on whose got the more rounds

    parameters:
        df : dataframe of the general data

    returns:
        df : df with extra column
    """
    map_winners = []

    for i in range(0,len(df)-1,2):
        if df['total_rounds'].iloc[i] > df['total_rounds'].iloc[i+1]:
            map_winners.append(df['Team Name'].iloc[i])
            map_winners.append(df['Team Name'].iloc[i])
        else:
            map_winners.append(df['Team Name'].iloc[i+1])
            map_winners.append(df['Team Name'].iloc[i+1])
    
    df['map_winners'] = map_winners

    return df

def calculate_win_rate(df, scope = 'match'):
    """
    Function that calculate the win rate based on different scope (match, round, maps) for all the teams present in the dataset

    parameters:
        df : dataframe of the general data of the event at stake
        scope : string that only takes 3 possible values : "match", "map", "round"
    returns:
        win_rate: a dictionnary with the team names as keys and the win rate on the values
    """ 
    match scope:
        case "match":
            data = df.drop_duplicates(['Stage', 'Series','Team Name'])
            win_rates = {team : round(len(data[data['Team Name'] == team].where(data['Team Name'] == data['winner']).dropna()) / len(data[data['Team Name'] == team].dropna()),2) for team in list(set(data['Team Name']))}
            return win_rates
        case "map":
            data_round = df.drop_duplicates(['Team Name', 'Unique Enum'])[['Stage', 'Series', 'Map #','Team Name', 'rounds', 'winner']]
            data_round['rounds'] = data_round['rounds'].apply(lambda x: list(map(int, x.split(', '))))
            data_round['total_rounds'] = data_round['rounds'].apply(lambda x: sum(x))
            map_winners = set_map_winner(data_round)
            win_rates = {team : round(len(map_winners[map_winners['Team Name'] == team].where(map_winners['Team Name'] == map_winners['map_winners']).dropna()) / len(map_winners[map_winners['Team Name'] == team].dropna()),2) for team in list(set(df['Team Name']))}
            return win_rates
        case "round":
            data_round = df.drop_duplicates(['Team Name', 'Unique Enum'])[['Stage', 'Series', 'Map #','Team Name', 'rounds', 'winner']]
            data_round['rounds'] = data_round['rounds'].apply(lambda x: list(map(int, x.split(', '))))
            data_round['total_rounds'] = data_round['rounds'].apply(lambda x: sum(x))
            win_rates = {team : round(sum(data_round[data_round['Team Name'] == team].dropna()['total_rounds']) / data_round[data_round['Team Name'] == team].dropna()['rounds'].apply(len).sum(), 2) for team in list(set(df['Team Name']))}
            return win_rates
        case _:
            raise NameError

#endregion
    
#region AgentStatistiques
    
def agent_popularity(data, player_name):
    """
        Function that returns a dictionnary of most picked agent for a player

        parameter:
            data : dataframe extracted from the scraper
            player : name of the player
    """
    try:

        data_player = data[data['Player Name'] == player_name]

        agent_popularity = {
            'player': player_name,
            'played_agent' : {agent:0 for agent in list(set(data_player["Agent Name"]))}
            }

        for i in range(len(data_player)):
            agent_played = data_player.iloc[i]["Agent Name"]
            agent_popularity['played_agent'][agent_played] += 1
        
        return agent_popularity
  
    except NameError:
        print(f'{NameError} | agent_popularity search failed')

def calculate_action_agent(agent, data, average, action, side):
    """
    Functions that calculate the number of action by side

    parameter:
        name : name of the player | string
        data : dataframe of the retrieve data from the scraper
        average : boolean if true then calculate the average, sum otherwise
        action : either 'K' or 'D'
        side : ATK, DFS or full match
    
    return:
        report : a dictionnary with the name as key and the calculated value
    """
    report = {agent: 0}
    actions = []

    side_mapping = {'Total': 0, 'Side 1': 1, 'Side 2': 2}
    side_ = side_mapping.get(side, None)
    
    if side_ is None:
        side_ = 0
    
    action_ = action if action in ['K', 'D'] else 'K'
    
    for i, _ in enumerate(data):
        actions.append(int(data[action_].iloc[i].split('\n')[side_]))
    
    if average:
        report[agent] = calculate_average(actions)
    else:
        report[agent] = sum(actions)
    
    return report

def number_action_by_scope_by_agent(df, agent, action, average, side=None, scope=None, name=None):
    """
    Functions that calculate the number of action by side, by player, by scope and by agent

    parameter:
        df : dataframe of the retrieve data from the scraper
        agent : Agent played by the player to analyze | string
        average : boolean if true then calculate the average, sum otherwise
        scope : string representing the instance that is under study i.e the match or the all tournament set to None by default
        action : either 'K' or 'D'
        side : ATK, DFS or full match set to None by default
    
    return:
        report : a dictionnary with the names as keys and the calculated value for each name
    """
    try:
        data_played_agent = df[df["Agent Name"] == agent]
    except NameError:
        print(f'No such {agent} in the dataset : {NameError}')

    data_player_filtered_by_scope = filter_by_scope(data_played_agent, scope)
    report = calculate_action_agent(agent, data_player_filtered_by_scope, average, action, side)

    return report

#endregion

#region general

def calculate_composition_for_each_team(data, map_to_select=None):
    """ Function that calculates the composition of each team based on a map
        
        Parameter:
            data : general data scraped from general scraper
            map_to_select : a map to focalize the calculation
        
        Return:
            heatmap_matrix : a 2 dimensional array with dim1 : teams and dim2 : agents
            map_to_select : can be null otherwise it is a string
            teams : list of team's name 
            agents : list of agent played"""
    
    if map_to_select:
        data = data[data['Map Name'] == map_to_select]
    
    summary = {id_match : {map_match : {team_name : set(data[(data['Id'] == id_match) & (data['Map Name'] == map_match) & (data['Team Name'] == team_name)]['Agent Name']) for team_name in set(data[(data['Id'] == id_match) & (data['Map Name'] == map_match)]['Team Name'])} for map_match in set(data[data['Id'] == id_match]['Map Name'])} for id_match in set(data["Id"])}

    teams = set()
    agents = set()

    for match in summary.values():
        for map_name, map_data in match.items():
            for team_name, agents_set in map_data.items():
                teams.add(team_name)
                agents.update(agents_set)

    # Mapping agents to indices
    agent_to_index = {agent: i for i, agent in enumerate(sorted(agents))}
    team_to_index = {team: i for i, team in enumerate(sorted(teams))}

    # Create empty heatmap matrix
    heatmap_matrix = np.zeros((len(teams), len(agents)))

    # Fill in the heatmap matrix
    for match in summary.values():
        for map_data in match.values():
            for team_name, agents_set in map_data.items():
                for agent in agents_set:
                    heatmap_matrix[team_to_index[team_name], agent_to_index[agent]] += 1
    
    return heatmap_matrix, map_to_select, agents, teams
#endregion

#region Pick and Bans

def calculate_most_picked_map(data, data_type,team_name = None):
    """
    Function that return the repartition of the picked map among the tournament
    
    parameter:
        data: data pick and bans from the scraper
        data_type: either 'Picks' or 'Bans'
        team_name: either string or None to get the most picked map of a team or all teams respectively
    return:
        df_picked_map : dataframe from dictionnary with the map as key and the number of times it has been picked
    """
    picked_map = defaultdict(int)

    if team_name:
        for maps in data[data['Team Name'] == team_name].dropna()[data_type].apply(ast.literal_eval):
            for map in maps:
                picked_map[map] += 1

        df_picked_map= pd.DataFrame.from_dict(dict(picked_map), orient='index', columns=[f'number_{data_type}']).reset_index()
        df_picked_map.rename(columns={'index': 'map'}, inplace=True)
        return df_picked_map
    else:
        # Iterate over each map and increment its count in picked_map
        for maps in data[data_type].apply(ast.literal_eval):
            for map in maps:
                picked_map[map] += 1

        df_picked_map= pd.DataFrame.from_dict(dict(picked_map), orient='index', columns=[f'number_{data_type}']).reset_index()
        df_picked_map.rename(columns={'index': 'map'}, inplace=True)
        return df_picked_map

#endregion

#region Economy

def calculate_mean_economy(data, team=[], series=None, stage=None):
    """
    Function that calculate the mean economy (banks and buys) filtered on the team, the stage and the series
    Intentionally no conflict here 
    """
    if len(team)>0:
        teams = team
    else:
        teams = set(data['Team Name'])
        
    if series:
        data = data[data['Series'] == series]

    if stage:
        data = data[data['Stage'] == stage]
                
    banks_buys = {team : (round(np.mean(data[data['Team Name'] == team]['Bank'].apply(lambda x: np.mean(ast.literal_eval(x)))),2), round(np.mean(data[data['Team Name'] == team]['Buys'].apply(lambda x: np.mean(ast.literal_eval(x)))),2))for team in teams}

    return banks_buys

def calculate_std_economy(data, team=[], series=None, stage=None):
    """
    Function that calculate the standard deviation for the economy (banks and buys) filtered on the team, the stage and the series
    Intentionally no conflict here 
    """
    if len(team)>0:
        teams = team
    else:
        teams = set(data['Team Name'])
        
    if series:
        data = data[data['Series'] == series]

    if stage:
        data = data[data['Stage'] == stage]
                
    banks_buys = {team : (round(np.mean(data[data['Team Name'] == team]['Bank'].apply(lambda x: np.std(ast.literal_eval(x)))),2), round(np.mean(data[data['Team Name'] == team]['Buys'].apply(lambda x: np.std(ast.literal_eval(x)))),2))for team in teams}

    return banks_buys

def create_summary_rounds_dataset(data):
    """ 
    Function that summarize the Economy data for each teams with rounds statistics over the all tournament

    Parameters:
        data : economy data
    
    Return:
        df : return sum of all the rounds / team categories by economy
    """
    data['nb_rounds'] = data['Bank'].apply(lambda x : len(ast.literal_eval(x)))
    
    summary_rounds = {team : (data.loc[data['Team Name'] == team,['Pistol_Won']].sum().values[0],
                            2 * len(data.loc[data['Team Name'] == team]),
                                data.loc[data['Team Name'] == team,['Eco_Won']].sum().values[0],
                                data.loc[data['Team Name'] == team,['Eco']].sum().values[0],
                                data.loc[data['Team Name'] == team,['$_Won']].sum().values[0],
                                data.loc[data['Team Name'] == team,['$']].sum().values[0],
                                data.loc[data['Team Name'] == team,['$$_Won']].sum().values[0],
                                data.loc[data['Team Name'] == team,['$$']].sum().values[0],
                                data.loc[data['Team Name'] == team,['$$$_Won']].sum().values[0],
                                data.loc[data['Team Name'] == team,['$$$']].sum().values[0],
                                data.loc[data['Team Name'] == team,['nb_rounds']].sum().values[0]) for team in set(data['Team Name'])}
    
    df = pd.DataFrame.from_dict(summary_rounds, orient='index', columns=['Pistol_Won','Pistol',
        'Eco_Won','Eco', '$_Won', '$', '$$_Won', '$$', '$$$_Won', '$$$', 'nb_rounds'])
    # Reset index to have the index as a separate column
    df.reset_index(inplace=True)
    # Rename the index column to 'key'
    df.rename(columns={'index': 'Team Name'}, inplace=True)

    return df

def create_ratio_economy_rounds(data):
    """ 
    Function that creates a dataframe with winrate for each Eco's, light buys, semi buys and full buys 
        as well as the ratio of eco rounds, light buys, semi buys and full buys
    
    Parameter:
        data : dataframe from create_summary_rounds_dataset()

    Return:
        df with added feature : ratio_pistol_won, ratio_eco_won, ratio_$_won, ratio_$$_won, ratio_$$$_won, ratio_eco, ratio_$, ratio_$$, ratio_$$$
    """

    # deal with null denominators 
    data['Pistol'] = data['Pistol'].replace(0,1)
    data['Eco'] = data['Eco'].replace(0,1)
    data['$'] = data['$'].replace(0,1)
    data['$$'] = data['$$'].replace(0,1)
    data['$$$'] = data['$$$'].replace(0,1)

    # ratio 
    data['ratio_pistol_won'] = round(data['Pistol_Won'] / data['Pistol'], 2)
    data['ratio_eco_won'] = round(data['Eco_Won'] / data['Eco'], 2)
    data['ratio_$_won'] = round(data['$_Won'] / data['$'], 2)
    data['ratio_$$_won'] = round(data['$$_Won'] / data['$$'], 2)
    data['ratio_$$$_won'] = round(data['$$$_Won'] / data['$$$'], 2)
    data['ratio_Eco'] = round(data['Eco'] / data['nb_rounds'], 3)
    data['ratio_$'] = round(data['$'] / data['nb_rounds'], 3)
    data['ratio_$$'] = round(data['$$'] / data['nb_rounds'], 3)
    data['ratio_$$$'] = round(data['$$$'] / data['nb_rounds'], 3)

    return data

#endregion

#region Performance

def total_individual_exploit(performance):
    """ Function that calculate the total number of individual exploit for each player throughout the tournament."""
    
    performance.replace(np.nan, '[]', inplace=True)
    names = set(performance['Player Name'])

    total_2K = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['2K'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_3K = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['3K'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_4K = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['4K'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_5K = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['5K'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_1v1 = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['1v1'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_1v2 = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['1v2'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_1v3 = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['1v3'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_1v4 = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['1v4'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}
    total_1v5 = {name : ( performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name]['1v5'].apply(lambda x: len(ast.literal_eval(x))).sum()) for name in names}

    list_totals = [total_2K, total_3K, total_4K, total_5K, total_1v1, total_1v2, total_1v3, total_1v4, total_1v5]
    list_name = ['2K', '3K', '4K', '5K', '1v1', '1v2', '1v3', '1v4', '1v5']
    df_totals = []

    for i,total in enumerate(list_totals):
        # Convert dictionary to DataFrame
        df_total = pd.DataFrame.from_dict(total, orient='index', columns=['team', list_name[i]]).reset_index()
        # Rename index column to 'player'
        df_total.rename(columns={'index': 'player'}, inplace=True)
        # Add to list
        df_totals.append(df_total)

    return df_totals

def ratio_individual_exploit(performance, data_type, economy, tot_rounds=False):
    """ Function that calculates the ratio of action X in the total number of round throughout the tournament.
        
        Parameter:
            total_X : dictionnary from total_individual_exploit() 
            economy : dataframe from economy_data_scraper()
            tot_rounds : boolean set to false, if we want to return the total number of round played
        
        Return:
            Dict : key is Player Name and value is ratio or (ratio, total rounds played) depending on tot_rounds"""
    
    performance.replace(np.nan, '[]', inplace=True)
    
    ActionRatio_eco = {name : [performance[performance['Player Name'] == name][data_type].apply(lambda x: len(ast.literal_eval(x))),
                              performance[performance['Player Name'] == name]['Team Name'],
                              performance[performance['Player Name'] == name]['Map #'],
                              performance[performance['Player Name'] == name]['Stage'],
                              performance[performance['Player Name'] == name]['Series']] for name in set(performance['Player Name'])}
    dict_name_ratio = {}

    for keys,values in ActionRatio_eco.items():
        tot_x = sum(values[0])
        team = list(values[1])[0]
        tot_rounds = 0
        for i in range(len(values[0])):
            rounds_played = economy.loc[(economy['Team Name'] == list(values[1])[i])
                                            & (economy['Map #'] == list(values[2])[i])
                                            & (economy['Stage'] == list(values[3])[i])
                                            & (economy['Series'] == list(values[4])[i])]['Bank']
            nbr_rounds_played = len(ast.literal_eval(list(rounds_played)[0]))
            tot_rounds+=nbr_rounds_played
        

        dict_name_ratio[keys] = (team,tot_x/tot_rounds)
    
    # Convert dictionary to DataFrame
    df_total = pd.DataFrame.from_dict(dict_name_ratio, orient='index', columns=['team', data_type]).reset_index()
    # Rename index column to 'player'
    df_total.rename(columns={'index': 'player'}, inplace=True)

    return df_total

def calculate_econ_per_player(performance):
    """ Function that calculates the mean Econ Rating = Damage / (Credits * 1000) """
    names = set(performance['Player Name'])

    mean_econ = {name : (performance[performance['Player Name'] == name]['Team Name'].iloc[0], round(performance[performance['Player Name'] == name]['ECON'].mean(),2)) for name in names}

    # Convert dictionary to DataFrame
    df_total = pd.DataFrame.from_dict(mean_econ, orient='index', columns=['team', 'ECON']).reset_index()
    # Rename index column to 'player'
    df_total.rename(columns={'index': 'player'}, inplace=True)

    return df_total

def calculate_spike_action(performance, data_type, total):

    """ Function that calculate the number of spike action
    
        Parameter:
            performance : performance data for scraping
            data_type : a string either 'PL' or 'DE' 
            total : either the total number of action if true or the ratio."""

    names = set(performance['Player Name'])

    if total:
        data = {name : (performance[performance['Player Name'] == name]['Team Name'].iloc[0], performance[performance['Player Name'] == name][data_type].mean().sum()) for name in names}
    else:
        data = {name : (performance[performance['Player Name'] == name]['Team Name'].iloc[0], round(performance[performance['Player Name'] == name][data_type].mean(),2)) for name in names}

    # Convert dictionary to DataFrame
    df_total = pd.DataFrame.from_dict(data, orient='index', columns=['team', data_type]).reset_index()
    # Rename index column to 'player'
    df_total.rename(columns={'index': 'player'}, inplace=True)

    return df_total
#endregion

#region Scraping

def create_id_column(df):
    """ Function that create an Id column in General data"""
    id_column = []
    prev_values = None
    current_id = 0

    for index, row in df.iterrows():
        current_values = row[['winner', 'Stage', 'Series']]
        if prev_values is None or not prev_values.equals(current_values):
            current_id += 1
        id_column.append(current_id)
        prev_values = current_values

    df['Id'] = id_column
    return df

def extract_round_numbers_if_present(text):
    """ Extract the round in the performance table from the text : Round X --> X """
    if 'Round' in text:
        round_numbers = re.findall(r'Round (\d+)', text)
        return [int(round_number) for round_number in round_numbers]
    else:
        return text

def convert_to_number(s):
    if s.endswith('k'):
        return int(float(s[:-1]) * 1000)
    elif s:
        return int(float(s))
    else:
        return None

def get_economy_data(table_economy_general):

    general_econ = []

    for _, row in enumerate(table_economy_general.find_all('tr')[1:]):
        data = row.find_all('td')
        team = data[0].text.strip()
        pistol_won = data[1].text.strip()
        Eco, Eco_Won = re.findall(r'\d+', data[2].text.strip())[0], re.findall(r'\d+', data[2].text.strip())[1]
        Semi_Eco, Semi_Eco_Won = re.findall(r'\d+', data[3].text.strip())[0], re.findall(r'\d+', data[3].text.strip())[1]
        Semi_Buy, Semi_Buy_Won = re.findall(r'\d+', data[4].text.strip())[0], re.findall(r'\d+', data[4].text.strip())[1]
        Full_Buy, Full_Buy_Won = re.findall(r'\d+', data[5].text.strip())[0], re.findall(r'\d+', data[5].text.strip())[1]

        general_econ.append([team, pistol_won, Eco, Eco_Won, Semi_Eco, Semi_Eco_Won, Semi_Buy, Semi_Buy_Won, Full_Buy, Full_Buy_Won])

    return general_econ[0], general_econ[1]

def get_banking_data(bank):

    banks = [[],[]]
    buys = [[],[]]

    for _, row in enumerate(bank.find_all('tr')):

        data = row.find_all('td')[1:]
        
        for column in data:
            # Extract text from each div element and also from comments and store in a list
            extracted_data = [element.get_text(strip=True) for element in column if element.string and element.string.strip() != ""]

            # Find all comments and extract the text from them
            comment_text = [comment.string.strip() for comment in column.find_all(text=lambda text: isinstance(text, Comment))]

            # find the commented part of the page
            div_text = [BeautifulSoup(item, 'html.parser').get_text(strip=True) for item in comment_text if item.startswith('<div>')]

            combined_data = extracted_data + div_text

            # remove empty string
            transformed_data = [item for item in combined_data if item.strip()] 

            # Remove elements containing '$' or the round retrieved
            filtered_data = [item for item in transformed_data if '$' not in item]

            # transform into integers
            transformed_lists = [convert_to_number(element) for element in filtered_data[1:]]

            # gather data
            banks[0].append(transformed_lists[0])
            banks[1].append(transformed_lists[1])
            buys[0].append(transformed_lists[2])
            buys[1].append(transformed_lists[3])
    
    return banks, buys

def create_economy_row(general_data1, general_data2, bank, buys, series, stage, map_num, map_name):
    """ 
    Build a row with that header : ["Team Name", "Map #", "Map Name", "Stage", "Series", "Pistol_Won", "Eco", "Eco_Won", "$", "$_Won", "$$", "$$_Won", '$$$', '$$$_Won', "Bank", "Buys"]
    """
    row1, row2 = [], []

    # Team Name
    row1.append(general_data1[0])
    row2.append(general_data2[0])

    # Map #
    row1.append(map_num+1)
    row2.append(map_num+1)

    # Map Name
    row1.append(map_name)
    row2.append(map_name)

    # Stage
    row1.append(stage)
    row2.append(stage)

    # Series
    row1.append(series)
    row2.append(series)

    # general economic data
    row1.extend(general_data1[1:])
    row2.extend(general_data2[1:])

    # Bank
    row1.append(bank[0])
    row2.append(bank[1])

    # Buys
    row1.append(buys[0])
    row2.append(buys[1])
    
    return row1, row2

def reorganize_phrases(phrases):
    """
    Process the phrases like : C9 ban Split; NRG ban Bind; C9 pick Sunset; NRG pick Ascent; C9 ban Breeze; NRG ban Icebox; Lotus remains
    into a list of two lists with the corresponding values (team name, map(s) banned, map(s) picked, remaining map )
    """
    team_map = {}

    decider = phrases[-1].strip().split(' ')[0]
    
    for i, phrase in enumerate(phrases):
        
        if i != len(phrases) - 1:
            
            parts = phrase.strip().split()
            team = parts[0]
            action = parts[1]
            
            if team not in team_map:
                team_map[team] = {'banned': [], 'picked': [], 'remaining': []}
            if action == 'ban':
                team_map[team]['banned'].append(parts[2])
            elif action == 'pick':
                team_map[team]['picked'].append(parts[2])


    result = []
    for team, maps in team_map.items():
        result.append([team, maps['banned'], maps['picked'], [decider]])

    return result

def reorganize_rounds_based_on_titles(scoring_one_by_one_for_all):
    """
    title[N-1] - title[N] -> [1,0] get the score of the round N based on the previous score and the actual score
    """
    team1_score, team2_score = [],[]
    for i in range(len(scoring_one_by_one_for_all)):
        if i==0:
            scores = scoring_one_by_one_for_all[i].split('-')
            team1_score.append(int(scores[0]))
            team2_score.append(int(scores[1]))
        else:
            # calculate scores
            previous_scores = scoring_one_by_one_for_all[i-1].split('-')
            actual_scores = scoring_one_by_one_for_all[i].split('-')
            team1_score.append(int(actual_scores[0]) - int(previous_scores[0]))
            team2_score.append(int(actual_scores[1]) - int(previous_scores[1]))
    return [team1_score, team2_score]

def save_match_data(url, type_of_data, data):
    """
    Save the dataframe as CSV into the correct directory...
    """
    event = url.split('/')[-2]

    name_of_data = type_of_data + "_data_" + event + ".csv"

    if not os.path.exists(event +'_data'):
        os.makedirs(event +'_data')
    
    file_path = os.path.join(event +'_data', name_of_data)

    data.to_csv(file_path, index=False)

    print(f"DataFrame saved as CSV file: {file_path}")

#endregion   

#region plotly in report
    
@st.cache_data
def plot_bar_individual_data(data, data_type, top_players, mean = None, std = None, colored_by = None):
    """
    Function that plots the bar chart of the dataframe of the general data for individual statistics from general data (cf. e.g. calculate_average_adr_player)

    parameters:
        data : dictionnary with key : player name, value : (team name, average score) (cf. e.g. calculate_average_adr_player)
        data_type : type of the data we want to display (rating, kills, deaths, adr, ...)
        top_players : int | number of top players that needs to be displayed
        mean : shows the mean value
        std : show the std high/low edges
        colored_by : ?
    """

    data_sorted = data.sort_values(by=data_type, ascending=False)

    fig_maps = px.bar(
        data_sorted.head(top_players),
        x= data_type,
        y="player",
        color='team')

    if mean:
        mean = data[data_type].mean()

        fig_maps.add_shape(
            type="line",
            x0=mean,
            y0=-0.5,
            x1=mean,
            y1=top_players,
            line=dict(
                color="black",
                width=2,
                dash="dot",
            )
        )
        
        if std :
            std = data[data_type].std()
            fig_maps.add_shape(
                type="line",
                x0=mean+std,
                y0=-0.5,
                x1=mean+std,
                y1=top_players,
                line=dict(
                    color="red",
                    width=1,
                    dash="dot",
                )
            )
            if mean - std > 0:
                fig_maps.add_shape(
                    type="line",
                    x0=mean-std,
                    y0=-0.5,
                    x1=mean-std,
                    y1=top_players,
                    line=dict(
                        color="red",
                        width=1,
                        dash="dot",
                    ))

    st.plotly_chart(fig_maps, theme="streamlit", use_container_width=True)

@st.cache_data
def plot_bar_picks_bans(data, data_type):
    """
    Function that plots the bar chart of the dataframe of the general data for individual statistics from general data (cf. e.g. calculate_average_adr_player)

    parameters:
        data : dictionnary with key : player name, value : (team name, average score) (cf. e.g. calculate_average_adr_player)
        data_type : type of the data we want to display (Picks, Bans)
    """
    fig_maps = px.bar(
        data,
        x='map',
        y=data_type,
        color=data_type,
        color_continuous_scale="reds")
    
    st.plotly_chart(fig_maps, theme="streamlit", use_container_width=True)

def plot_average_economy(data, mean=None, std=None):

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Bank', 'Buys']).reset_index()
    df = df.rename(columns={'index': 'Team'})

    # Plot the bar chart using Plotly Express
    fig = px.bar(df, x='Team', y=['Bank', 'Buys'], barmode='group', title='Bank and Loadout by Team')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

def display_charts_two_teams(show_diff_bank, show_diff_buys, team, bank_a, bank_b, buys_a, buys_b):

    diff_bank = [bank_a[i] - bank_b[i] for i in range(len(bank_a))]
    diff_buys = [buys_a[i] - buys_b[i] for i in range(len(buys_a))]

    d = {f'diff_bank_{team[0]}-{team[1]}': diff_bank, f'diff_loadout_{team[0]}-{team[1]}': diff_buys}

    df = pd.DataFrame(d)

    if show_diff_bank and show_diff_buys:
        st.area_chart(df, use_container_width=True)
    elif show_diff_bank:
        st.area_chart(df[f'diff_bank_{team[0]}-{team[1]}'],use_container_width=True)
    elif show_diff_buys:
        st.area_chart(df[f'diff_loadout_{team[0]}-{team[1]}'], use_container_width=True)
    else:
        st.write("Please select at least one chart to display.")

def display_charts_two_teams_2(show_diff_bank, show_diff_buys, team, bank_a, bank_b, buys_a, buys_b):

    diff_bank = [bank_a[i] - bank_b[i] for i in range(len(bank_a))]
    diff_buys = [buys_a[i] - buys_b[i] for i in range(len(buys_a))]

    d = {f'diff_bank_{team[0]}-{team[1]}': diff_bank, f'diff_loadout_{team[0]}-{team[1]}': diff_buys}

    df = pd.DataFrame(d)

    # Calculate mean of each column
    mean_diff_bank = np.mean(diff_bank)
    mean_diff_buys = np.mean(diff_buys)

    # Create a figure
    fig = go.Figure()

    if show_diff_bank:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'diff_bank_{team[0]}-{team[1]}'], mode='lines', name=f'diff_bank_{team[0]}-{team[1]}'))

    if show_diff_buys:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'diff_loadout_{team[0]}-{team[1]}'], mode='lines', name=f'diff_loadout_{team[0]}-{team[1]}'))

    # Add trace for mean values
    fig.add_trace(go.Scatter(x=df.index, y=[mean_diff_bank] * len(df.index), mode='lines', name='Mean diff_bank', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=[mean_diff_buys] * len(df.index), mode='lines', name='Mean diff_buys', line=dict(color='blue')))

    st.plotly_chart(fig, use_container_width=True)

def plot_bank_and_buys(data, stage, series, map_name, team=[]):
    
    if len(team) <= 1:

        fig = go.Figure()

        bank = ast.literal_eval(data.loc[(data['Stage'] == stage) & (data['Series'] == series) & (data['Map Name'] == map_name) & (data['Team Name'] == team[0])]['Bank'].values[0])
        buys = ast.literal_eval(data.loc[(data['Stage'] == stage) & (data['Series'] == series) & (data['Map Name'] == map_name) & (data['Team Name'] == team[0])]['Buys'].values[0])

        fig.add_trace(go.Scatter(x=list(range(1, len(bank)+1)), y=bank, mode='lines+markers', name=f'{team[0]} - Bank', visible='legendonly'))
        fig.add_trace(go.Scatter(x=list(range(1, len(bank)+1)), y=buys, mode='lines+markers',name=f'{team[0]} - Buys', visible='legendonly'))

        # Add buttons for selecting/deselecting series
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="down",
                    buttons=list([
                        dict(label="Show Bank",
                            method="update",
                            args=[{"visible": [True, False]}]),
                        dict(label="Show Buys",
                            method="update",
                            args=[{"visible": [False, True]}]),
                        dict(label="Show Both",
                            method="update",
                            args=[{"visible": [True, True]}]),
                        dict(label="Show None",
                            method="update",
                            args=[{"visible": [False, False]}])
                    ]),
                    x=0.1,
                    xanchor='left',
                    y=1.15,
                    yanchor='top',
                    bgcolor='rgba(255, 255, 255, 0.7)',
                    bordercolor='rgba(0, 0, 0, 0.5)',
                    borderwidth=1,
                    font=dict(family="Arial, sans-serif", size=10)
                )
            ],
            title='Bank and Loadout for Teams',
            xaxis_title='Match rounds',
            yaxis_title='Values',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(family="Arial, sans-serif"),
            plot_bgcolor='rgba(255,255,255,0)',
            paper_bgcolor='rgba(255,255,255,0.8)',
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True)
        )

        st.plotly_chart(fig)
    else:

        st.write(team)
        st.write(stage)
        st.write(series)
        st.write(map_name)
        
        bank_a = ast.literal_eval(data.loc[(data['Stage'] == stage) & (data['Series'] == series) & (data['Map Name'] == map_name) & (data['Team Name'] == team[0])]['Bank'].values[0])
        buys_a = ast.literal_eval(data.loc[(data['Stage'] == stage) & (data['Series'] == series) & (data['Map Name'] == map_name) & (data['Team Name'] == team[0])]['Buys'].values[0])

        bank_b = ast.literal_eval(data.loc[(data['Stage'] == stage) & (data['Series'] == series) & (data['Map Name'] == map_name) & (data['Team Name'] == team[1])]['Bank'].values[0])
        buys_b = ast.literal_eval(data.loc[(data['Stage'] == stage) & (data['Series'] == series) & (data['Map Name'] == map_name) & (data['Team Name'] == team[1])]['Buys'].values[0])
        
        show_diff_bank = st.sidebar.checkbox("Show diff_bank")
        show_diff_buys = st.sidebar.checkbox("Show diff_buys")

        display_charts_two_teams(show_diff_bank, show_diff_buys, team, bank_a, bank_b, buys_a, buys_b)

def plot_rounds_economy(data, round_type, mean=None, std=None):
    """ """ 
    fig_maps = px.bar(
        data,
        x='Team Name',
        y=round_type,
        color=round_type,
        color_continuous_scale="reds")
    
    st.plotly_chart(fig_maps, theme="streamlit", use_container_width=True)

def plot_composition_for_each_team(heatmap_matrix, map_to_select, agents, teams):

    # Plotting the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_matrix, cmap="YlOrRd", annot=True, fmt=".0f", xticklabels=sorted(agents), yticklabels=sorted(teams), ax=ax)
    ax.set_xlabel('Agents')
    ax.set_ylabel('Teams')
    if map_to_select:
        ax.set_title(f'Agent Composition by Team and Match on {map_to_select}')
    else:
        ax.set_title('Agent Composition by Team and Match')

    # Display the plot in Streamlit
    st.pyplot(fig)
#endregion

#region Display in UI
def display_individual_statistics(data, metric_name, type_calculated='total', mean=True, std=True):

    """ Function that display the plot of the individual statistics in the UI adding a button that control the ranges.
    
        Parameter:
            data: this is a dataframe (likewise calculate_average_fk_players)
            metric_name : name of the metric '1v2', 'ADR', 'ACS','4K'...
            mean & std : true by default """
    
    top_X = st.number_input(f"Select the top X player for {metric_name} ({type_calculated}) : ", value=0, step=1, format="%d")
    is_not_set = False
    count_greater_than_zero = 0

    if top_X == 0:
        #by default
        st.caption(f"Total {metric_name} of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Total {metric_name} of the top {int(top_X)} players ({type_calculated})")

    if is_not_set:
        for i in range(len(data)):
            if data[metric_name].iloc[i] > 0:
                count_greater_than_zero += 1
        top_X = min(15,count_greater_than_zero)

    plot_bar_individual_data(data, metric_name, top_X, mean, std)

#endregion  

#region Dataset Generation

def normalize_data(df):
    """ Function that normalize the data """
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()

    # Fit and transform the data
    df_normalized = scaler.fit_transform(df)

    # Convert the result back to a DataFrame
    df_normalized = pd.DataFrame(df_normalized, columns=df.columns, index=df.index)

    return df_normalized
    
def create_dataframe(df_emea, df_americas, df_pacific, to_normalize=True):
    """ Function that creates the features X and the target y 
        
        Parameter:
            df_emea: dataframe for the feature selected for the EMEA region
            df_americas: dataframe for the feature selected for the AMERICAS region
            df_pacific: dataframe for the feacture selected for the PACIFIC region"""

    # df_emea, df_americas, and df_pacific are dataframes for each region
    # Concatenate the dataframes vertically to create a single dataframe
    df_concatenated = pd.concat([df_emea, df_americas, df_pacific], keys=['EMEA', 'Americas', 'Pacific'])

    if to_normalize:
        # normalize data
        df_concatenated = normalize_data(df_concatenated)

    return df_concatenated

def parse_value(x, index, default):

    split_values = x.strip().split('\n')

    if (len(split_values) > index) and (len(split_values[index]) > 0):
        return float(split_values[index])
    else:
        return default

def parse_hs_value(x, index, default):

    split_values = x.strip().split('\n')

    if (len(split_values) > index) and (len(split_values[index][:-1]) > 0):
        return float(split_values[index][:-1])
    else:
        return default

def general_feature_creation_for_teams(general, list_feature = ['R', 'ACS', 'K', 'D','ADR', 'HS%', 'FK']):

    """
        Function that creates a dataframe of the average/std features for a region with the general data. Individual feature only. 

        Parameter:
            general : dataframe from the scraper general_data_scraper
            list_feature : list of feature to compute
    """

    teams_of_regions = set(general['Team Name'])

    gathered_feature_name = []
    gathered_dictionnaries = []

    for feature_name in list_feature:

        if feature_name == 'HS%':

            default = np.mean(general[feature_name].apply(lambda x : float(x.strip().split('\n')[0][:-1])).values)
            # Action
            avrg_action_per_team = {team : np.mean(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_hs_value(x, 0, default))) for team in teams_of_regions}
            std_action_per_team = {team : np.std(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_hs_value(x, 0, default))) for team in teams_of_regions}
            # Action attack
            avrg_action_per_team_atk = {team : np.mean(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_hs_value(x, 1, default))) for team in teams_of_regions}
            std_action_per_team_atk = {team : np.std(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_hs_value(x, 1, default))) for team in teams_of_regions}
            # Action defense
            avrg_action_per_team_dfs = {team : np.mean(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_hs_value(x, 2, default))) for team in teams_of_regions}
            std_action_per_team_dfs = {team : np.std(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_hs_value(x, 2, default))) for team in teams_of_regions}
        else:
            default = np.mean(general[feature_name].apply(lambda x : float(x.strip().split('\n')[0])).values)
            # Action
            avrg_action_per_team = {team : np.mean(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_value(x, 0, default))) for team in teams_of_regions}
            std_action_per_team = {team : np.std(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_value(x, 0, default))) for team in teams_of_regions}
            # Action attack
            avrg_action_per_team_atk = {team : np.mean(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_value(x, 1, default))) for team in teams_of_regions}
            std_action_per_team_atk = {team : np.std(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_value(x, 1, default))) for team in teams_of_regions}
            # Action defense
            avrg_action_per_team_dfs = {team : np.mean(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_value(x, 2, default))) for team in teams_of_regions}
            std_action_per_team_dfs = {team : np.std(general[general['Team Name'] == team][feature_name].apply(lambda x : parse_value(x, 2, default))) for team in teams_of_regions}

        gathered_dictionnaries.append(avrg_action_per_team)
        gathered_feature_name.append(f'avrg_{feature_name.lower()}_per_team')
        gathered_dictionnaries.append(std_action_per_team)
        gathered_feature_name.append(f'std_{feature_name.lower()}_per_team')
        gathered_dictionnaries.append(avrg_action_per_team_atk)
        gathered_feature_name.append(f'avrg_{feature_name.lower()}_per_team_atk')
        gathered_dictionnaries.append(std_action_per_team_atk)
        gathered_feature_name.append(f'std_{feature_name.lower()}_per_team_atk')
        gathered_dictionnaries.append(avrg_action_per_team_dfs)
        gathered_feature_name.append(f'avrg_{feature_name.lower()}_per_team_dfs')
        gathered_dictionnaries.append(std_action_per_team_dfs)
        gathered_feature_name.append(f'std_{feature_name.lower()}_per_team_dfs')
    
    # Create an empty DataFrame
    df = pd.DataFrame(columns=gathered_feature_name)

    # Iterate over the list of dictionaries
    for team in gathered_dictionnaries[0].keys():
        # Create a new row for each team
        row_values = [d[team] for d in gathered_dictionnaries]
        df.loc[team] = row_values
    
    return df

def performance_feature_creation_for_teams(performance, economy, 
                                            features_ratio = ['2K', '3K', '4K', '5K', '1v1', '1v2', '1v3','1v4', '1v5'],
                                            features_mean = ['ECON','PL','DE']):
    """ Function that calculate the feature creation for each performance dataframe"""
    values = {'team': []}

    for feature in features_ratio:
        # Gather data
        df = ratio_individual_exploit(performance, feature, economy)
        # Calculate mean per team
        mean_per_team = df.groupby('team')[feature].mean()
        std_per_team = df.groupby('team')[feature].std()

        # Store mean values in the dictionary
        values[f'{feature.lower()}_mean'] = mean_per_team.values
        values['team'] = mean_per_team.index.tolist() 
        values[f'{feature.lower()}_std'] = std_per_team.values
        #values['team'] = std_per_team.index.tolist() 


    df = pd.DataFrame(values)

    # Calculate mean for features_mean and add to DataFrame
    for feature in features_mean:
        # Gather data and calculate mean per team
        mean_per_team = performance.groupby('Team Name')[feature].mean()
        std_per_team = performance.groupby('Team Name')[feature].std()
        
        # Add mean values to DataFrame
        df[f'{feature.lower()}_mean'] = mean_per_team[df['team']].values
        df[f'{feature.lower()}_std'] = std_per_team[df['team']].values
    
    df.set_index('team', inplace=True)
    
    return df

def economy_feature_creation_for_teams(economy):
    """ Function that create the dataframe with selected feature for the economic data for each region """

    # Economic rounds ratio
    summary_economy_rounds = create_summary_rounds_dataset(economy)
    columns_to_drop = summary_economy_rounds.columns[1:][:-1]
    ratio = create_ratio_economy_rounds(summary_economy_rounds)
    ratio_dropped = ratio.drop(columns=columns_to_drop)
    ratio_dropped.set_index('Team Name', inplace=True)

    # Bank and Buys
    bank_and_buys = calculate_mean_economy(economy)
    ratio_dropped['Bank'] = ratio_dropped.index.map(lambda x: bank_and_buys[x][0])
    ratio_dropped['Buys'] = ratio_dropped.index.map(lambda x: bank_and_buys[x][1])

    return ratio_dropped
#endregion
    
#region Feature Selection for Analysis
    
def selectKbest(X,y,k=10):
    """ Fonction that select the k best features (for explainability) """
    
    # Initialize SelectKBest with the desired number of features
    selector = SelectKBest(score_func=f_classif, k=k)
    # Fit the selector to the data
    selector.fit(X, y)
    # Get the indices of the selected features
    selected_indices = selector.get_support(indices=True)
    # Get the names of the selected features
    selected_features = X.columns[selected_indices]
    feature_scores = selector.scores_[selected_indices]

    # Print names and scores for selected features
    for feature, score in zip(selected_features, feature_scores):
        print(f"Feature '{feature}': {score}")

    return selected_features

def RFECV_feature_selection(X,y, krnl="linear"):

    # Create a Support Vector Classifier as the estimator
    estimator = SVC(kernel=krnl)
    # Create RFECV object
    rfecv = RFECV(estimator=estimator, cv=StratifiedKFold(5), scoring='accuracy')  # 5-fold cross-validation
    # Fit RFECV to the data
    rfecv.fit(X, y)
    # Get selected features
    selected_indices = rfecv.support_
    # Get names of selected features
    selected_features = X.columns[selected_indices]

    # Print selected features
    print("Selected Features:")
    print(selected_features)

    # Print optimal number of features
    print("Optimal number of features: {}".format(rfecv.n_features_))

    return selected_features

#endregion
    
#region Visualize Data for analysis

def visualize_mean_feature_for_each_region(df_concatenated, discriminating_feature):
    """ Fonction that visualize the data for the three region"""

    # Calculate the mean of each column for each region
    mean_per_region = df_concatenated.groupby(level=0).mean()

    filtered_dataframe = mean_per_region[discriminating_feature]

    # Plot the mean of each column for each region
    for column in filtered_dataframe.columns:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(filtered_dataframe.index, filtered_dataframe[column])
        ax.set_title(f"Mean of {column} by Region")
        ax.set_ylabel("Mean")
        ax.set_xlabel("Region")
        ax.grid(True)
        plt.tight_layout()
        plt.savefig(f"analysis\mean_{column}_by_region.png")  # Save each plot to a PNG file
        plt.close(fig)  # Close the figure to free up memory

    print("Plots saved as PNG files.")

def plot_t_sne(X,y,n=2):
    # Perform t-SNE with 2 components
    tsne = TSNE(n_components=n, random_state=42)
    X_tsne = tsne.fit_transform(X)

    # Plot t-SNE embeddings
    plt.figure(figsize=(10, 8))
    for region in np.unique(y):
        plt.scatter(X_tsne[y == region, 0], X_tsne[y == region, 1], label=region)
    plt.title("t-SNE Visualization of Data with Region Labels")
    plt.xlabel("t-SNE Component 1")
    plt.ylabel("t-SNE Component 2")
    plt.legend()
    plt.show()

#endregion 