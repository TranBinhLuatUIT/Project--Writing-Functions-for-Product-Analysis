import pandas as pd
def categorize_nps(x):
    """ Take a NPS rating and outputs whether it's a "promoter" , "passive", "detractor"
    or invalid. Rating is 0 to 10
    
    Args:
        x(int) : NPS Rating 
        
    Returns:
        string: The NPS Category or Invalid
    """
    if x >= 0 and x <= 6:
        return "detractor"
    elif x >= 7 and x <= 8  :
        return "passive"
    elif x >= 9 and x <= 10:
        return "promoter"
    else:
        return "invalid"
#test
# categorize_nps(6)
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

# print(check_csv("datasets/corrupted.csv"))

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
    temp = df['nps_rating'].apply(categorize_nps)
    df['nps_group'] = temp
    return df

#test function, convert mobile csv to dataframe
# print(convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile"))
#It workes, so in the future, if I have any dataset from another source, I can easily create dataframe for it

       
def combine_nps_csvs(csvs_dict):
    """Combine all csv file together to a dataframe from a dictionary 

    Args:
        csvs_dict(dict) : contain key (path to your csv), value (source of this csv) 

    Returns:
        DataFrame

    """
    combined = pd.DataFrame()
    for key,value in csvs_dict.items():
        if(check_csv(key)):
            temp = convert_csv_to_df(key, value)
            combined = pd.concat([combined,temp])
        else:
                print(value + " is not valid")
    return combined


# #test combine_nps_csvs
# df = combine_nps_csvs(csv_dict)

def calculate_nps(df):
    """Calculate NPS score from nps_group with appearance's number of promoter and detractor
    
    Args:
        df(DataFrame) : A DataFrame which is converted from combined CSV
        
    Return:
        float: NPS Score
    """
    d = df['nps_group'].value_counts()
    
    return (d['promoter'] - d['detractor'])/sum(d)*100

# Test the function on the  dictionary
# q4_nps = combine_nps_csvs(csv_dict)
# calculate_nps(q4_nps)

def calculate_nps_by_score(df):
    """Calculate NPS Score for each Source
    
    Args:
        df(DataFrame): DataFrame which is converted from combined CSV, include many source
        
    Return:
        Series: NPS Scores broken by souce
    """
    
    # Group the DataFrame by source and apply calculate_nps()
    result = df.groupby(df['source']).apply(calculate_nps)
    # Return a Series with the NPS scores broken by source
    return result

def calculate_nps_by_date(df):
    """Calculate NPS Score for each date to find out when people rate detractor too much
    
    Args:
        df(DataFrame): DataFrame which is converted from combined CSV, include many source
        
    Return:
        Series: NPS Scores broken by date
    """
    return df.groupby(df['response_date']).apply(calculate_nps)
#######################################################################
#Finally, This is my workflow:

#First, I define a dictionary that contain all csv path and source_type
csv_dict = {
  "datasets/2020Q4_nps_email.csv": "email",
  "datasets/2020Q4_nps_mobile.csv": "mobile",
  "datasets/2020Q4_nps_web.csv": "web",
  "datasets/corrupted.csv": "social_media"
}

#Second, I check every csv before converted to DaTaFrame and add column source_type for each datafram. Then I combine all file
df = combine_nps_csvs(csv_dict)

#Then, I calculate nps score from all source. So We can conclude where we should improve more
print(calculate_nps_by_score(df))

#I wanna check whether any time that User rate many detractor ?
groupby_date = calculate_nps_by_date(df)