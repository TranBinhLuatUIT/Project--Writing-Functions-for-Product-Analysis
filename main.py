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
print(convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile"))
#It workes, so in the future, if I have any dataset from another source, I can easily create dataframe for it

#I have to check whether my csv file is valid (have 3 column response_date, user_id, nps_rating)
def check_csv(path):
    """Check whether your csv file include 3 column response_date, user_id, nps_rating or not

    Args:
        path(string) : path to your csv file
        
    Return:
        bool: True if csv have 3 column, False if not
        
    """
    #use context manager with
    with open(path) as f:
        first_line = f.readline()
        if (first_line == "response_date,user_id,nps_rating\n"):
            return True
        else: return False

print(check_csv("datasets/corrupted.csv"))
        
    