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




