import streamlit as st
import pandas as pd


st.set_page_config(page_title="Economic Data", page_icon="$$")

economic_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/economy_data_champions-tour-2024-pacific-kickoff.csv')

st.text('Economic Data')
st.write(economic_data)


