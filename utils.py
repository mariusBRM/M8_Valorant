import pandas as pd

# Set general constant
SIDE = {'Total' : 0, 'Side 1' : 1, 'Side 2' : 2}
NAME = ['logaN', 'Wailers', 'beyAz', 'TakaS', 'nataNk']
TEAM = "Gentle Mates"

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
    Functions that calculate the number of action by side by player and by scope

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
    

