import pandas as pd

def convert_csv_to_df(path, source_type):
    """Converst csv file to a dataframe, csv file is collect from many source (mobile, web, email)
    
    
    Args: 
        path(string) : A path to your csv file 
        
        source_type(string) : where we collected data from (mobile, web, email, ...) 

    Returns
        A DataFrame is converted by csv file and column 'source' 

    """
    
    df = pd.read_csv(path)
    df['source'] = source_type
    
    return df
#test function, convert mobile csv to dataframe

df = convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile")
    

