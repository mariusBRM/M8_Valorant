
# Set general constant
SIDE = {'Total' : 0, 'Side 1' : 1, 'Side 2' : 2}
NAME = ['logaN', 'Wailers', 'beyAz', 'TakaS', 'nataNk']

class BasicStatistique:

    #TODO: Change the return type of number_action_avg_by_player_by_scope in the case there are mutliple Names
    # should be able to get all of the change
    def average(list):
        return sum(list) / len(list)

    def number_action_avg_by_player_by_scope(self, df, scope, action, side, name = NAME):
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
            kills = df[df['Player Name'].isin(name)]
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

