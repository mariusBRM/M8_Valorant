import streamlit as st
import pandas as pd
from utils import *
import plotly.express as px

st.set_page_config(page_title="General Data", page_icon="general")

st.title('Data visualization of the general data of the Pacific KickOff 2024')
general_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/general_data_champions-tour-2024-pacific-kickoff.csv')

st.text('General Data')
st.write(general_data)

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
        color_continuous_scale="reds")

    st.plotly_chart(fig_maps, theme="streamlit", use_container_width=True)

with col3:
    st.caption("Win Rate Rounds")
    fig_rounds = px.bar(
        df_win_rates_rounds.sort_values(by="Win rate", ascending=False),
        x="Team",
        y="Win rate",
        color="Win rate",
        color_continuous_scale="reds")

    st.plotly_chart(fig_rounds, theme="streamlit", use_container_width=True)


st.subheader("Individual Statistics")

# Rating
ratings = calculate_average_rating_players(general_data)
st.caption("Average ratings of the top 15 players")
ratings_sorted = ratings.sort_values(by="rating", ascending=False)

fig_maps_rating = px.bar(
    ratings_sorted.head(15),
    x="rating",
    y="player",
    color='team')

st.plotly_chart(fig_maps_rating, theme="streamlit", use_container_width=True)

# Kills
kills = calculate_average_kills_players(general_data)
kills_sorted = kills.sort_values(by="kills", ascending=False)

st.caption("Average kills of the top 15 players")

fig_maps_kills = px.bar(
    kills_sorted.head(15),
    x="kills",
    y="player",
    color="team")

st.plotly_chart(fig_maps_kills, theme="streamlit", use_container_width=True)

# Deaths
deaths = calculate_average_death_players(general_data)
deaths_sorted = deaths.sort_values(by="deaths", ascending=True)

st.caption("Average death of the top 15 players (with least deaths)")

fig_maps_death = px.bar(
    deaths_sorted.head(15),
    x="deaths",
    y="player",
    color="team")

st.plotly_chart(fig_maps_death, theme="streamlit", use_container_width=True)

# ADR
adr = calculate_average_adr_players(general_data)
adr_sorted = adr.sort_values(by="adr", ascending=False)
st.caption("Average ADR of the top 15 players")

fig_maps_adr = px.bar(
    adr_sorted.head(15),
    x="adr",
    y="player",
    color="team")

st.plotly_chart(fig_maps_adr, theme="streamlit", use_container_width=True)
# HS
hs = calculate_average_hs_players(general_data)
df_hs = pd.DataFrame(list(hs.items()), columns=['player', 'hs'])
# First Kills
first_kills = calculate_average_fk_players(general_data)
df_fk = pd.DataFrame(list(first_kills.items()), columns=['player', 'first kill'])
# First Death
first_deaths = calculate_average_fd_players(general_data)
df_fd = pd.DataFrame(list(first_deaths.items()), columns=['player', 'first death'])




