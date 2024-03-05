import streamlit as st
import pandas as pd
import sys

sys.path.append('C:\\Users\\marius.reymauzaize\\Desktop\\Project\\M8_Valorant')

from utils import *

st.set_page_config(
    page_title="Report",
    page_icon="Valorant",
)

st.title("PRX in VCT Pacific Kick Off 2024!")

st.sidebar.success("Select a report above!")

st.image('icon\\vct_pacific_logo.png')