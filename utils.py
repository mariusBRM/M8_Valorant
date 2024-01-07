import pandas as pd

# Set general constant
SIDE = {'Total' : 0, 'Side 1' : 1, 'Side 2' : 2}
NAME = ['logaN', 'Wailers', 'beyAz', 'TakaS', 'nataNk']
TEAM = "Gentle Mates"
class BasicStatistics:

    #TODO: Change the return type of number_action_avg_by_player_by_scope in the case there are mutliple Names
    # should be able to get all of the change
    def __init__(self):
        self.side = {'Total' : 0, 'Side 1' : 1, 'Side 2' : 2}

    def calculate_action_player(self, name, data, average, action, side):
        """ 
        Function that calculate the average action  (kills/death) of a player for a given side (attack, defense or total) 
        returns the name and the average kill of the player
        """
        report = {name : 0}
        actions = []

        try:
            side_ = self.side[side]
        except NameError:
            raise NameError(f'No side named {side}')
        
        if action not in ['K', 'D']:
            action_ = 'K'
        else:
            action_ = action
        
        for i,value in enumerate(data):
            actions.append(int(data[action_].iloc[i].split('\n')[side_]))
        
        if average:
            report[name] = self.average(actions)
        else:
            report[name] = sum(actions)
        return report
    
    def calculate_action_team(self, names, data, average, action, side):
        """ 
        Function that calculate the average action  (kills/death) of a player for a given side (attack, defense or total) 
        returns the name and the average kill of each player of the team
        """
        report = {n:[] for n in names}
        
        try:
            side_ = self.side[side]
        except NameError:
            raise NameError(f'No side named {side}')
        
        if action not in ['K', 'D']:
            action_ = 'K'
        else:
            action_ = action

        for i,value in enumerate(data):
            name = value['Player Name']
            report[name].append(int(data[action_].iloc[i].split('\n')[side_]))
        
        if average:
            final_report = {n:self.average(report[n]) for n in names}
        else:
            final_report = {n:sum(report[n]) for n in names}
        return final_report
    
    def filter_by_scope(self, data, scope):

        if scope:
            # the scope is specified
            try:
                data = data[data["Series"] == scope]
                return data
            except NameError:
                print(f'side {scope} is not specified so return the all data.')
                return data
        else:
            # by default the all dataset
            return data
        
    def average(list):
        return sum(list) / len(list)

    def number_action_by_player_by_scope(self, df, action, average,side = None, scope = None, name = None, team_name = None):
        """
            Function that calculates the average kill/death of each player by scope

            parameter:
                df : data set
                scope : string, 'Tournament' for the all, values in the column Series for discretized
                action : string 'K', 'D'
                side : string 'Total', 'Side 1', 'Side 2'
        """

        if name is not None:
            # want statistic on a particular player
            try:
                data_player = df[df['Player Name'] == name]
            except NameError:
                print(f'No such {name} in the dataset : {NameError}')
            data_player_filtered_by_scope = self.filter_by_scope(data_player, scope)
            report_player = self.calculate_action_player(name, data_player_filtered_by_scope,average,action, side)

            return report_player

        elif team_name is not None:
            # want statistic on the all team
            try:
                set_names = set(df['Player Name'].where(df['Team Name'] == team_name))
            except NameError:
                print(f'No such {set_names} in the dataset : {NameError}')

            names = pd.DataFrame(list(set_names), columns=['Player']).dropna()['Player'].values.tolist()
            data_team = df[df['Player Name'].isin(names)]
            data_team_filtered_by_scope = self.filter_by_scope(data_team, scope)
            report_team = self.calculate_action_team(names,data_team_filtered_by_scope, average,action, side)

            return report_team
        else:
            raise NameError('No instance can be treated')
    

