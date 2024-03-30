import streamlit as st
import pandas as pd
from utils import *

st.set_page_config(page_title="Economic Data", page_icon="$$")

economic_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/economy_data_champions-tour-2024-pacific-kickoff.csv')

st.text('Economic Data')
st.write(economic_data)

selected_teams = st.multiselect("Select Teams", list(set(economic_data['Team Name'])))

if len(selected_teams) > 2:
    selected_teams = selected_teams[:2]

# empty => Overall overview
if len(selected_teams) == 0:

    data = calculate_mean_economy(economic_data)
    plot_average_economy(data)

elif len(selected_teams) == 1:
    
    data = calculate_mean_economy(economic_data, selected_teams)
    select_matches = st.multiselect("Select Match", list(set(economic_data.loc[economic_data['Team Name'] == selected_teams[0], ['Stage', 'Series', 'Team Name']].apply(lambda x: (x['Stage'],x['Series']), axis=1))))

    if len(select_matches) > 0:

        select_maps = st.multiselect("Select Map", list(economic_data.loc[(economic_data['Team Name'] == selected_teams[0]) & (economic_data['Stage'] == select_matches[0][0]) & (economic_data['Series'] == select_matches[0][1])]['Map Name']))

        if len(select_maps) > 0:
            select_maps = select_maps[0]
            plot_bank_and_buys(economic_data, select_matches[0][0], select_matches[0][1], select_maps, selected_teams)
    
    plot_average_economy(data)
else:
    
    data = calculate_mean_economy(economic_data, selected_teams)

    matches_team_a = set(economic_data.loc[(economic_data['Team Name'] == selected_teams[0]), ['Stage', 'Series', 'Team Name']].apply(lambda x: (x['Stage'],x['Series']), axis=1))
    matches_team_b = set(economic_data.loc[(economic_data['Team Name'] == selected_teams[1]), ['Stage', 'Series', 'Team Name']].apply(lambda x: (x['Stage'],x['Series']), axis=1))
    common_matches = list(matches_team_a.intersection(matches_team_b))
    select_matches = st.multiselect("Select Match",common_matches)
    
    if len(select_matches) > 0:

        select_maps = st.multiselect("Select Map", list(economic_data.loc[(economic_data['Team Name'] == selected_teams[0]) & (economic_data['Stage'] == select_matches[0][0]) & (economic_data['Series'] == select_matches[0][1])]['Map Name']))

        if len(select_maps) > 0:
            select_maps = select_maps[0]
            plot_bank_and_buys(economic_data, select_matches[0][0], select_matches[0][1], select_maps, selected_teams)
    
    plot_average_economy(data)
# len == 1 => display different matches + overall overview on all matches of that team
# len == 2 => display different matches 

