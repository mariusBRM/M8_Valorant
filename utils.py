import pandas as pd

# Set general constant
SIDE = {'Total' : 0, 'Side 1' : 1, 'Side 2' : 2}
NAME = ['logaN', 'Wailers', 'beyAz', 'TakaS', 'nataNk']
TEAM = "Gentle Mates"
class BasicStatistics:

    #TODO: Change the return type of number_action_avg_by_player_by_scope in the case there are mutliple Names
    # should be able to get all of the change
    def calculate_action_player(self, name, data, action, side):
        report = {name : 0}
        try:
            side_ = SIDE[side]
        except NameError:
            raise NameError(f'No side named {side}')
        
        if action not in ['K', 'D']:
            action_ = 'K'
        else:
            action_ = action
        
        #TODO: continue
        return 0
    
    def calculate_action_team(self, names, data, action, side):
        report = {n:0 for n in names}


        return 0
    
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

    def number_action_avg_by_player_by_scope(self, df, action, side = None, scope = None, name = None, team_name = None):
        """
            Function that calculates the average kill/death of each player by scope

            parameter:
                df : data set
                scope : string, 'Tournament' for the all, values in the column Series for discretized
                action : string 'K', 'D'
                side : string 'Total', 'Side 1', 'Side 2'
        """
        try:
            processed_kills = []
            if name:
                # want statistic on a particular player
                data_player = df[df['Player Name'] == name]
                data_player_filtered_by_scope = self.filter_by_scope(data_player, scope)
                report_player = self.calculate_action_player(data_player_filtered_by_scope, action, side)

            elif team_name:
                # want statistic on the all team
                set_names = set(df['Player Name'].where(df['Team Name'] == team_name))
                names = pd.DataFrame(list(set_names), columns=['Player']).dropna()['Player'].values.tolist()
                data_team = df[df['Player Name'].isin(names)]
                data_team_filtered_by_scope = self.filter_by_scope(data_team, scope)
                report_team = self.calculate_action_team(data_team_filtered_by_scope, action, side)
            else:
                raise NameError('No instance can be treated')
            
            

            if scope != "Tournament" and scope in set(kills['Series']):
                # average in a particular Match
                kills = kills[kills['Series'] == scope]
                for i in range(len(kills)):
                    processed_kills.append(int(kills[action].iloc[i].split('\n')[SIDE[side]]))
                return self.average(processed_kills)    
            elif scope == "Tournament":
                # average in the all Tournament
                for i in range(len(kills)):
                    processed_kills.append(int(kills[action].iloc[i].split('\n')[SIDE[side]]))
                return self.average(processed_kills)
            else:
                print(f'{scope} is not available or mispelled')
                
        except NameError:
            print(f'Cannot fetch kills because {NameError}')

    def number_action_by_player_by_scope(df, scope, action, side, name = NAME):
        """Function that calculates the kills/deaths of each player by scope

            parameter:
                df : data set
                scope : string, 'Tournament' for the all, values in the column Series for discretized
                action : string 'K', 'D'
        """
        try:
            processed_kills = []
            kills = df[df['Player Name'].isin(name)]
            if scope != "Tournament" and scope in set(kills['Series']):
                # average in a particular Match
                kills = kills[kills['Series'] == scope]
                for i in range(len(kills)):
                    processed_kills.append(int(kills[action].iloc[i].split('\n')[SIDE[side]]))
                return processed_kills   
            elif scope == "Tournament":
                # average in the all Tournament
                for i in range(len(kills)):
                    processed_kills.append(int(kills[action].iloc[i].split('\n')[SIDE[side]]))
                return processed_kills
            else:
                print(f'{scope} is not available or mispelled')
                
        except NameError:
            print(f'Cannot fetch kills because {NameError}')

    def ratio_kill_death(self, df, scope, side):
        """
            Function that calculates the average kill/death ratio of each player by scope

            parameter:
                df : data set
                scope : string, 'Tournament' for the all, values in the column Series for discretized
                side : string 'Total', 'Side 1', 'Side 2'
        """
        try:
            processed_kills = []
            ratio = []
            kills = df[df['Player Name'].isin(NAME)]
            if scope != "Tournament" and scope in set(kills['Series']):
                # average in a particular Match
                kills = kills[kills['Series'] == scope]
                for i in range(len(kills)):
                    processed_kills.append(int(kills['K'].iloc[i].split('\n')[SIDE[side]]))
                return self.average(processed_kills)    
            elif scope == "Tournament":
                # average in the all Tournament
                for i in range(len(kills)):
                    processed_kills.append(int(kills['K'].iloc[i].split('\n')[SIDE[side]]))
                return self.average(processed_kills)
            else:
                print(f'{scope} is not available or mispelled')
        except NameError:
            print(f'Cannot fetch kills because {NameError}')

