import os
import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler
from utils import *
import sys


#region EMEA specific processing

def replace_koi_value(column):
    return column.str.replace('Movistar KOI\t\t\t\t\t\t\n\t\t\t\t\t\t\t(KOI)', 'KOI')

def fix_koi_naming(df):
    df['Team Name'] = replace_koi_value(df['Team Name'])
    return df

#endregion

#region Data Normalization

def normalize_data(df):
    """ Function that normalize the data """
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()

    # Fit and transform the data
    df_normalized = scaler.fit_transform(df)

    # Convert the result back to a DataFrame
    df_normalized = pd.DataFrame(df_normalized, columns=df.columns, index=df.index)

    return df_normalized

#endregion
