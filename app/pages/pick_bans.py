import streamlit as st
import pandas as pd
from utils import *
st.set_page_config(page_title="Pick & Bans", page_icon="pick_and bans")

region = st.session_state['region']

# "EMEA", "Pacific", "Americas"
if region == 'Pacific':
    pick_bans = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/pick_ban_data_data_champions-tour-2024-pacific-kickoff.csv')
elif region == 'EMEA':
    pick_bans = pd.read_csv('../champions-tour-2024-emea-kickoff_data/pick_ban_data_data_champions-tour-2024-emea-kickoff.csv')
elif region == 'Americas':
    pick_bans = pd.read_csv('../champions-tour-2024-americas-kickoff_data/pick_ban_data_champions-tour-2024-americas-kickoff.csv')


st.text('Picks & Bans')
st.write(pick_bans)

# Define a list of button labels
button_labels = ['All']
button_labels += list(set(pick_bans['Team Name']))
team_to_analyze = None

# Initialize a variable to store the selected button
selected_button = None

num_rows = (len(button_labels) - 1) // 6 + 1

# Create buttons dynamically based on the list length and arrange them in rows
for i in range(num_rows):
    row = st.columns(min(6, len(button_labels) - i * 6))  # Each row contains at most 6 buttons
    for j in range(min(6, len(button_labels) - i * 6)):
        with row[j]:
            if st.button(button_labels[i * 6 + j]):
                if button_labels[i * 6 + j] != 'All':
                    team_to_analyze = button_labels[i * 6 + j]

picks = calculate_most_picked_map(pick_bans, 'Picks', team_to_analyze)
bans = calculate_most_picked_map(pick_bans, 'Bans', team_to_analyze)

st.caption(f"Map picked")
plot_bar_picks_bans(picks, 'number_Picks')

st.caption(f"Map banned")
plot_bar_picks_bans(bans, 'number_Bans')