import streamlit as st
import pandas as pd
from utils import *


st.set_page_config(page_title="Performance Data", page_icon="performance")

performance_data = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/performance_data_champions-tour-2024-pacific-kickoff.csv')

st.text('Performance Data')
st.write(performance_data)

display_option = st.radio("Select Display Option", ("Total individual action", "Individual action rate"))



def display_individual_total_action():

    total_2K, total_3K, total_4K, total_5K, total_1v1, total_1v2, total_1v3, total_1v4, total_1v5 = total_individual_exploit(performance_data)
    # 2Ks
    display_individual_statistics(total_2K, '2K')

    # 3Ks
    display_individual_statistics(total_3K, '3K')
    
    # 4Ks
    display_individual_statistics(total_4K, '4K')

    # 5Ks
    display_individual_statistics(total_5K, '5K')

    # 1v1s
    display_individual_statistics(total_1v1, '1v1')

    # 1v2s
    display_individual_statistics(total_1v2, '1v2')

    # 1v3s
    display_individual_statistics(total_1v3, '1v3')

    # 1v4s
    display_individual_statistics(total_1v4, '1v4')

    # 1v5s
    display_individual_statistics(total_1v5, '1v5')


def display_individual_action_rate():
    
    economy = pd.read_csv('../champions-tour-2024-pacific-kickoff_data/economy_data_champions-tour-2024-pacific-kickoff.csv')

    ratio_2K = ratio_individual_exploit(performance_data,'2K',economy)
    # 2Ks
    display_individual_statistics(ratio_2K, '2K', 'ratio')

    ratio_3K = ratio_individual_exploit(performance_data,'3K',economy)
    # 3Ks
    display_individual_statistics(ratio_3K, '3K', 'ratio')
    
    ratio_4K = ratio_individual_exploit(performance_data,'4K',economy)
    # 4Ks
    display_individual_statistics(ratio_4K, '4K', 'ratio')

    ratio_5K = ratio_individual_exploit(performance_data,'5K', economy)
    # 5Ks
    display_individual_statistics(ratio_5K, '5K', 'ratio')

    ratio_1v1 = ratio_individual_exploit(performance_data, '1v1',economy)
    # 1v1s
    display_individual_statistics(ratio_1v1, '1v1', 'ratio')

    ratio_1v2 = ratio_individual_exploit(performance_data, '1v2',economy)
    # 1v2s
    display_individual_statistics(ratio_1v2, '1v2', 'ratio')

    ratio_1v3 = ratio_individual_exploit(performance_data, '1v3',economy)
    # 1v3s
    display_individual_statistics(ratio_1v3, '1v3', 'ratio')

    ratio_1v4 = ratio_individual_exploit(performance_data, '1v4',economy)
    # 1v4s
    display_individual_statistics(ratio_1v4, '1v4', 'ratio')

    ratio_1v5 = ratio_individual_exploit(performance_data,'1v5',economy)
    # 1v5s
    display_individual_statistics(ratio_1v5, '1v5', 'ratio')


if display_option == "Total individual action":
    display_individual_total_action()
elif display_option == "Individual action rate":
    display_individual_action_rate()
