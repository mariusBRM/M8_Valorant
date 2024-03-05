import streamlit as st
import pandas as pd

st.set_page_config(page_title="Performance Data", page_icon="performance")

performance_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/performance_data_champions-tour-2024-pacific-kickoff.csv')

st.text('Performance Data')
st.write(performance_data)