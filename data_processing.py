import os
import pandas as pd
import lxml
import requests  
from bs4 import BeautifulSoup, Comment
import re
from utils import *
import sys


#region EMEA processing

def replace_koi_value(column):
    return column.str.replace('Movistar KOI\t\t\t\t\t\t\n\t\t\t\t\t\t\t(KOI)', 'KOI')

def fix_koi_naming(df):
    df['Team Name'] = replace_koi_value(df['Team Name'])
    return df

#endregion
