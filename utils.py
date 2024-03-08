import pandas as pd
import os
import re
from bs4 import BeautifulSoup, Comment

# Set general constant
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

def calculate_average_rating_players(df, side = None):
    """ 
    Function that calculate the average rating of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['R'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['R'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['R'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    else:
        print(f'Side is either None, ATK or DFS')

def calculate_average_kills_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['K'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['K'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['K'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    else:
        print(f'Side is either None, ATK or DFS')

def calculate_average_death_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['D'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['D'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['D'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    else:
        print(f'Side is either None, ATK or DFS')

def calculate_average_adr_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['ADR'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['ADR'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['ADR'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    else:
        print(f'Side is either None, ATK or DFS')

def calculate_average_hs_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['HS%'].apply(lambda x: float(x.split('\n')[0][:-1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['HS%'].apply(lambda x: float(x.split('\n')[1][:-1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['HS%'].apply(lambda x: float(x.split('\n')[2][:-1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    else:
        print(f'Side is either None, ATK or DFS')

def calculate_average_fk_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['FK'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['FK'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['FK'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    else:
        print(f'Side is either None, ATK or DFS')

def calculate_average_fd_players(df, side=None):
    """ 
    Function that calculate the average kills of the players on a filtered by side 

    parameters:
        df: dataframe of the general data
        side: string that takes one of the following values : None (for the total), ATK for attacking and DFS for defense
    """
    if side is None:
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['FK/FD +/'].apply(lambda x: float(x.split('\n')[0]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'ATK':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['FK/FD +/'].apply(lambda x: float(x.split('\n')[1]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
    elif side == 'DFS':
        average_rating_scores = {player : round(sum(df[df['Player Name'] == player].dropna()['FK/FD +/'].apply(lambda x: float(x.split('\n')[2]))) / len(df[df['Player Name'] == player].dropna()), 2) for player in list(set(df['Player Name']))}
        return average_rating_scores
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
            data_round = df.drop_duplicates(['Stage', 'Series','Team Name', 'Map #'])[['Stage', 'Series', 'Map #','Team Name', 'rounds', 'winner']]
            data_round['rounds'] = data_round['rounds'].apply(lambda x: list(map(int, x.split(', '))))
            data_round['total_rounds'] = data_round['rounds'].apply(lambda x: sum(x))
            map_winners = set_map_winner(data_round)
            win_rates = {team : round(len(map_winners[map_winners['Team Name'] == team].where(map_winners['Team Name'] == map_winners['map_winners']).dropna()) / len(map_winners[map_winners['Team Name'] == team].dropna()),2) for team in list(set(df['Team Name']))}
            return win_rates
        case "round":
            data_round = df.drop_duplicates(['Stage', 'Series','Team Name', 'Map #'])[['Stage', 'Series', 'Map #','Team Name', 'rounds', 'winner']]
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

#region Scraping

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
