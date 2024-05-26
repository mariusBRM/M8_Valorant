import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import streamlit as st
import pandas as pd
from utils import *

st.set_page_config(
    page_title="Report",
    page_icon="Valorant",
)


display_option = st.radio("Select Region", ("EMEA", "Pacific", "Americas"))

st.session_state['region'] = display_option

def display_emea():
    st.title("VCT EMEA Kick Off 2024!")

    st.image('icon\\vct_emea_logo.png')

def display_pacific():

    st.title("VCT Pacific Kick Off 2024!")

    st.image('icon\\vct_pacific_logo.png')

def display_americas():
    
    st.title("VCT Americas Kick Off 2024!")

    st.image('icon\\vct_americas_logo.png')

if display_option == "EMEA":
    display_emea()
elif display_option == "Pacific":
    display_pacific()
elif display_option == "Americas":
    display_americas()

