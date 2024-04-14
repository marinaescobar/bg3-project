import pandas as pd
import numpy as np

def missing_data_cleaning (df , type):

    df.dropna(how='all', inplace=True)
    
    if 'type' == 'armor':
    
        min_no_nulls = int(0.75 * len(df.columns))
        
        df.dropna(thresh=min_no_nulls, inplace=True)
    
    else:
        
        min_no_nulls = int(0.25 * len(df.columns))
    
        df.dropna(thresh=min_no_nulls, inplace=True)
    
    df = df.reset_index()
    
    df.drop('index', axis=1, inplace=True)
    
    return df