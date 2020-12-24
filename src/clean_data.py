import numpy as np
import pandas as pd

def split_columns(data):
    df = pd.read_json(data)

    # access dictionary values, create new columns and drop parents
    snippet = []
    contentDetails = []
    statistics = []
    columns = ['snippet', 'contentDetails', 'statistics']
    new_dfs = [snippet, contentDetails, statistics]
    for item, new_df in zip(columns, new_dfs):
        new_df.append(pd.json_normalize(df[item]))
    new_df = pd.concat([df, snippet[0], contentDetails[0], statistics[0]], axis=1)
    new_df.drop(columns=columns, inplace=True)
    new_df.drop(columns=['_id'], inplace=True)
    new_df.set_index('id', inplace=True)
    
    # un-nest 'tags' column
    new_df['tags'] = new_df['tags'].apply(lambda x: ', '.join(map(str, x)) if type(x)==list else np.nan)
    
    # cast numeric string values to float, pad NaN values
    columns_ = ['categoryId', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount']
    for column in columns_:
        new_df[column] = new_df[column].apply(lambda x: int(x) if type(x)==str else np.nan)
        new_df[column].fillna(method='pad', inplace=True)
    
    return new_df

if __name__ == '__main__':
    data = '../data/yoga_uncleaned.json'
    new_df = split_columns(data)
    new_df.to_csv('../data/yoga.csv')