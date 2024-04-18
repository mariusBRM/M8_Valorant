import streamlit as st
import pandas as pd
from utils import *
import plotly.express as px

st.set_page_config(page_title="General Data", page_icon="general")

if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()

st.title('Data visualization of the general data of the Pacific KickOff 2024')
general_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/general_data_champions-tour-2024-pacific-kickoff.csv')

st.text('General Data')
st.write(general_data)

display_option = st.radio("Select Display Option", ("General & Individual statistics", "Map composition"))

def display_general_individual_statistics():
    """ Function that display the information of the individual statistics overall"""
    st.subheader("Win rates of each team")

    # calculate win rate
    win_rate_matches = calculate_win_rate(general_data,scope='match')
    win_rate_maps = calculate_win_rate(general_data,scope='map')
    win_rate_rounds = calculate_win_rate(general_data,scope='round')

    # create dataframes win rates
    df_win_rates_matches = pd.DataFrame(list(win_rate_matches.items()), columns=['Team', 'Win rate'])
    df_win_rates_maps = pd.DataFrame(list(win_rate_maps.items()), columns=['Team', 'Win rate'])
    df_win_rates_rounds = pd.DataFrame(list(win_rate_rounds.items()), columns=['Team', 'Win rate'])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Win Rate Matches")
        fig_matches = px.bar(
            df_win_rates_matches.sort_values(by="Win rate", ascending=False),
            x="Team",
            y="Win rate",
            color="Win rate",
            color_continuous_scale="reds")

        st.plotly_chart(fig_matches, theme="streamlit", use_container_width=True)

    with col2:
        st.caption("Win Rate Maps")
        fig_maps = px.bar(
            df_win_rates_maps.sort_values(by="Win rate", ascending=False),
            x="Team",
            y="Win rate",
            color="Win rate",
            color_continuous_scale="blues")

        st.plotly_chart(fig_maps, theme="streamlit", use_container_width=True)

    with col3:
        st.caption("Win Rate Rounds")
        fig_rounds = px.bar(
            df_win_rates_rounds.sort_values(by="Win rate", ascending=False),
            x="Team",
            y="Win rate",
            color="Win rate",
            color_continuous_scale="purples")

        st.plotly_chart(fig_rounds, theme="streamlit", use_container_width=True)


    st.subheader("Individual Statistics")

    top_ratings = st.number_input("Select the top X player to analyze for rating", value=0, step=1, format="%d")
    is_not_set = False
    # Rating
    ratings = calculate_average_rating_players(general_data)
    if top_ratings == 0:
        #by default
        st.caption(f"Average ratings of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Average ratings of the top {int(top_ratings)} players")

    if is_not_set:
        top_ratings = 15

    plot_bar_individual_data(ratings, "rating", top_ratings, True, True)


    # Kills
    kills = calculate_average_kills_players(general_data)

    top_kills = st.number_input("Select the top X player to analyze for kills", value=0, step=1, format="%d")
    is_not_set = False

    if top_kills == 0:
        #by default
        st.caption(f"Average kills of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Average kills of the top {int(top_kills)} players")

    if is_not_set:
        top_kills = 15

    plot_bar_individual_data(kills, "kills", top_kills, True, True)


    # Deaths
    deaths = calculate_average_death_players(general_data)

    top_deaths = st.number_input("Select the top X player to analyze for deaths", value=0, step=1, format="%d")
    is_not_set = False

    if top_deaths == 0:
        #by default
        st.caption(f"Average deaths of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Average deaths of the top {int(top_deaths)} players")

    if is_not_set:
        top_deaths = 15

    plot_bar_individual_data(deaths, "deaths", top_deaths, True, True)

    # ADR
    adr = calculate_average_adr_players(general_data)

    top_adr = st.number_input("Select the top X player to analyze for ADR", value=0, step=1, format="%d")
    is_not_set = False

    if top_adr == 0:
        #by default
        st.caption(f"Average ADR of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Average ADR of the top {int(top_adr)} players")

    if is_not_set:
        top_adr = 15

    plot_bar_individual_data(adr, "adr", top_adr, True, True)

    # HS
    hs = calculate_average_hs_players(general_data)

    top_hs = st.number_input("Select the top X player to analyze for headshot rate", value=0, step=1, format="%d")
    is_not_set = False

    if top_hs == 0:
        #by default
        st.caption(f"Average headshot rate of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Average headshot rate of the top {int(top_hs)} players")

    if is_not_set:
        top_hs = 15

    plot_bar_individual_data(hs, "hs", top_hs, True, True)

    # First Kills
    first_kills = calculate_average_fk_players(general_data)

    top_fk = st.number_input("Select the top X player to analyze for first kill", value=0, step=1, format="%d")
    is_not_set = False

    if top_fk == 0:
        #by default
        st.caption(f"Average first kills of the top 15 players")
        is_not_set = True
    else:
        st.caption(f"Average first kills of the top {int(top_hs)} players")

    if is_not_set:
        top_fk = 15

    plot_bar_individual_data(first_kills, "fk", top_fk, True, True)


def display_map_composition():
    """ Function that display the map composition for each team based on the map"""
    # Define a list of button labels
    button_labels = ['All']
    button_labels += list(set(general_data['Map Name']))
    map_to_analyze = None

    # Initialize a variable to store the selected button
    selected_button = None

    num_rows = (len(button_labels) - 1) // 4 + 1

    # Create buttons dynamically based on the list length and arrange them in rows
    for i in range(num_rows):
        row = st.columns(min(4, len(button_labels) - i * 4))  # Each row contains at most 6 buttons
        for j in range(min(4, len(button_labels) - i * 4)):
            with row[j]:
                if st.button(button_labels[i * 4 + j]):
                    if button_labels[i * 4 + j] != 'All':
                        map_to_analyze = button_labels[i * 4 + j]
                        
    heatmap_matrix, map_to_select, agents, teams = calculate_composition_for_each_team(general_data, map_to_analyze)
    plot_composition_for_each_team(heatmap_matrix, map_to_select, agents, teams)


if display_option == "General & Individual statistics":
    display_general_individual_statistics()
elif display_option == "Map composition":
    display_map_composition()





