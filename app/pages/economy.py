import streamlit as st
import pandas as pd
from utils import *

st.set_page_config(page_title="Economic Data", page_icon="$$")

region = st.session_state['region']

# "EMEA", "Pacific", "Americas"
if region == 'Pacific':
    economic_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/economy_data_champions-tour-2024-pacific-kickoff.csv')
elif region == 'EMEA':
    economic_data = pd.read_csv('../champions-tour-2024-emea-kickoff_data/economy_data_champions-tour-2024-emea-kickoff.csv')
elif region == 'Americas':
    economic_data = pd.read_csv('../champions-tour-2024-americas-kickoff_data/economy_data_champions-tour-2024-americas-kickoff.csv')

st.text('Economic Data')
st.write(economic_data)

display_option = st.radio("Select Display Option", ("Bank & Buys", "Rounds economy"))

def display_bank_buys():

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

def display_rounds_economy():

    selected_teams = st.multiselect("Select Teams", list(set(economic_data['Team Name'])))
    
    # general (not categorized by map)
    summary_economic_rounds = create_summary_rounds_dataset(economic_data)
    ratios = create_ratio_economy_rounds(summary_economic_rounds)

    if len(selected_teams) >= 1:
        ratios = ratios[ratios['Team Name'].isin(selected_teams)]
    
    # 'ratio_pistol_won','ratio_eco_won', 'ratio_$_won', 'ratio_$$_won', 'ratio_$$$_won','ratio_Eco', 'ratio_$', 'ratio_$$', 'ratio_$$$'
    plot_rounds_economy(ratios, 'ratio_pistol_won')

    plot_rounds_economy(ratios, 'ratio_eco_won')

    plot_rounds_economy(ratios, 'ratio_$_won')

    plot_rounds_economy(ratios, 'ratio_$$_won')

    plot_rounds_economy(ratios, 'ratio_$$$_won')

    plot_rounds_economy(ratios, 'ratio_Eco')

    plot_rounds_economy(ratios, 'ratio_$')

    plot_rounds_economy(ratios, 'ratio_$$')

    plot_rounds_economy(ratios, 'ratio_$$$')


if display_option == "Bank & Buys":
    display_bank_buys()
elif display_option == "Rounds economy":
    display_rounds_economy()