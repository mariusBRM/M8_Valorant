import streamlit as st
import pandas as pd

st.set_page_config(page_title="General Data", page_icon="general")

general_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/general_data_champions-tour-2024-pacific-kickoff.csv')

st.text('General Data')
st.write(general_data)