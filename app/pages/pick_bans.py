import streamlit as st
import pandas as pd
from utils import *
st.set_page_config(page_title="Pick & Bans", page_icon="pick_and bans")

pick_bans = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/pick_ban_data_champions-tour-2024-pacific-kickoff.csv')

st.text('Picks & Bans')
st.write(pick_bans)

picks = calculate_most_picked_map(pick_bans, 'Picks')
bans = calculate_most_picked_map(pick_bans, 'Bans')

st.caption(f"Map picked")
plot_bar_picks_bans(picks, 'number_Picks')

st.caption(f"Map banned")
plot_bar_picks_bans(bans, 'number_Bans')