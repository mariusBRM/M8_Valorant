import os
import pandas as pd
import lxml
import requests  
from bs4 import BeautifulSoup
import re

def extract_round_numbers_if_present(text):
    if 'Round' in text:
        round_numbers = re.findall(r'Round (\d+)', text)
        return [int(round_number) for round_number in round_numbers]
    else:
        return text

def matches_scraper(url):
    return 0

def general_data_scraper(list_url):
    """
    Function that extract the general data from a vlr.gg url (page of a match between two teams)
    The general data aims the overview display in the vlr.gg page and gather the data displayed in the tables in a textual form

    parameter:
        list_url : list of url representing the different matches
    
    return:
        result : a dataframe of all the extracted data flatten
    """

    match_stats = []

    for matchnum in range(len(list_url)):

        url = list_url[matchnum]
        
        source_match = requests.get(url=url).text
        soup_match = BeautifulSoup(source_match, features="html.parser")
        
        table_match = soup_match.findAll('table', {'class':'wf-table-inset mod-overview'})

        stage = soup_match.findAll('div', {'class':'match-header-event-series'})[0].text.strip().split(":", 1)[0]

        series = soup_match.findAll('div', {'class':'match-header-event-series'})[0].text.strip().split("\n", 1)[1].strip()

        winner = soup_match.findAll('div', {'class':'match-bet-item-team'})[0].text.strip().split("\n")[2].strip()
        
        for a in [a for a in list(range(len(table_match))) if a not in [2,3]]:
            if a in [0,1]:
                map_num = 1
            else:
                map_num = a//2
            
            map_name = soup_match.findAll('div', {'class':'vm-stats-gamesnav-item js-map-switch'})[map_num-1].text.strip()[1:].strip()
            stage = soup_match.findAll('div', {'class':'match-header-event-series'})[0].text.strip().split(":", 1)[0]
            team_name = soup_match.findAll('div', {'class':'wf-title-med'})[a % 2].text.strip()
            
            table = table_match[a]
            headers_match = []
            
            for i in table.find_all('th'):
                title_match = i.text.strip()
                headers_match.append(title_match)
                
            headers_match[0] = 'Player Name'
            headers_match[1] = 'Agent Name'
            headers_match[6] = 'K/D +/–'   
            headers_match[12] = 'FK/FD +/–'   
            df_match = pd.DataFrame(columns=headers_match)
            
            for row in table.find_all('tr')[1:]:
                data = row.find_all('td')
                row_data = [td.text.strip() for td in data]
                row_data[1] = str(data[1]).split('title="',1)[1].split('"',1)[0].title()
                length = len(df_match)
                df_match.loc[length] = row_data
            
            df_match['Team Name'] = team_name
            df_match['Map Name'] = map_name
            df_match['Map #'] = map_num
            df_match['Stage'] = stage
            df_match['Series'] = series
            df_match['winner'] = winner
            
            match_stats.append(df_match)
        

    result = pd.concat(match_stats).reset_index(drop=True)
    result['Player Name'] = result['Player Name'].str.split("\n").str[0].str.strip()
    result['D'] = result['D'].str[1:-1]
    result = result.apply(pd.to_numeric, errors='ignore')
    result.drop('KAST', axis=1, inplace = True)

    return result

def performance_data_scraper(list_url):

    match_stats = []

    for matchnum in range(len(list_url)):
        url = list_url[matchnum] + '/?game=all&tab=performance'
        
        source_match = requests.get(url=url).text
        soup_match = BeautifulSoup(source_match, features="html.parser")

        stage = soup_match.findAll('div', {'class':'match-header-event-series'})[0].text.strip().split(":", 1)[0]

        series = soup_match.findAll('div', {'class':'match-header-event-series'})[0].text.strip().split("\n", 1)[1].strip()

        table_performance = soup_match.findAll('table', {'class':'wf-table-inset mod-adv-stats'})

        for map_num in range(1, len(table_performance)):

            map_name = soup_match.findAll('div', {'class':'vm-stats-gamesnav-item js-map-switch'})[map_num-1].text.strip()[1:].strip()

            table = table_performance[map_num]

            headers_match = []
            
            for i in table.find_all('th'):
                title_match = i.text.strip()
                headers_match.append(title_match)
            
            headers_match[0] = 'Player Name'
            headers_match[1] = 'Map Name'
            headers_match.append('Team Name')

            df_match = pd.DataFrame(columns=headers_match)

            for i,row in enumerate(table.find_all('tr')[1:]):
                added_row = []
                data = row.find_all('td')
                row_data = [td.text for td in data]
                transformed_data = [extract_round_numbers_if_present(text.replace('\t','').strip()) for text in row_data]
                name_and_team = transformed_data[0].split('\n')
                transformed_data[0] = name_and_team[0]
                transformed_data.append(name_and_team[1])
                length = len(df_match)
                df_match.loc[length] = transformed_data
            
            df_match['Map Name'] = map_name
            df_match['Map #'] = map_num
            df_match['Stage'] = stage
            df_match['Series'] = series

            match_stats.append(df_match)
    
    result = pd.concat(match_stats).reset_index(drop=True)
    result = result.apply(pd.to_numeric, errors='ignore')
    
    return result

def economy_data_scraper(url):
    return 0