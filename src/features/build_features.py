import pandas as pd
import numpy as np

from constants import COURSES
from constants import LANGUAGES
from constants import LOCATIONS
from constants import UTM_MEDIUM
from constants import UTM_SOURCE

#PREPROCESSING FUNCTIONS

def change_to_datetime(df,column):
    df[column] = df[column].apply(pd.to_datetime).copy()
    return df

def change_format(df,column):
    df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def combine_columns(df, column1, column2, new_column):
    df[new_column] = df[column1].fillna('') + str(' ') + df[column2].fillna('')   
    return df

def drop_null_columns(df):
    df.dropna(axis=1, how='all', inplace=True)  
    return df

def drop_test_rows(df):
    df = df[df["email"].str.contains("@4geeks") == False]
    return df

def remove_duplicates(df):
    df = df.replace("Nan", np.nan)
    df = df.sort_values("created_at")
    df = df.groupby("email").first().reset_index()
    return df
    
def clean_course(df,column):
    for row in df:
        df[column] = df[column].replace(COURSES[course], course)
        print(df[column].value_counts())
    return df
 
def clean_location(df,column):
    for location in LOCATIONS:
        df[column] = df[column].replace(LOCATIONS[location], location)
        print(df[column].value_counts())
    return df
  
    
def clean_language(df,column):
    for language in LANGUAGES:
        df[column] = df[column].replace(LANGUAGES[language], language)
        print(df[column].value_counts())
    return df
    
def clean_utm_medium(df,column):
    for value in UTM_MEDIUM:
        df[column] = df[column].replace(UTM_MEDIUM[value], value)
        print(df[column].value_counts())
    return df      
    
def clean_utm_source(df):
    for value in UTM_SOURCE:
        df[column] = df[column].replace(UTM_SOURCE[value], value)
        print(df[column].value_counts())
    return df

def assign_lead_type(df,column1,column2):
    
    for row in df:
        if df[column1] == 'request_more_info': 
            df[column2] == 'SOFT'
        elif df[column1] == 'website-lead': 
            df[column2] == 'STRONG'
        elif df[column1] == 'newsletter': 
            df[column2] == 'DISCOVERY'
        elif df[column1] == 'contact-us': 
            df[column2] == 'SOFT'
        elif df[column1] == 'utec-uruguay': 
            df[column2] == 'STRONG'
        elif df[column1] == 'jobboard-lead': 
            df[column2] == 'STRONG'
        elif df[column1] == 'hiring-partner': 
            df[column2] == 'OTHER'
        elif df[column1] == 'download_outcome': 
            df[column2] == 'DISCOVERY'
        elif df[column1] == 'website-lead,blacks-in-technology': 
            df[column2] == 'STRONG'
        elif df[column1] == 'request_downloadable': 
            df[column2] == 'DISCOVERY'      
        else:   
            df[column2] == 'DISCOVERY'
    
    return df

def assign_with_conditions(df):
    df.loc[df['utm_source'] == 'landingjobs', 'utm_medium'] = 'referral',
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'Facebook_Mobile_Feed') & (df['has_gclid'] == '0') ,
                              'social', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_medium'] == 'Facebook_Mobile_Feed') & (df['has_gclid'] == '1') , 
                              'cpc', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_medium'] == '23849757712110143') & (df['has_gclid'] == '0') , 
                              'social', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_medium'] == '23849757712110143') & (df['has_gclid'] == '1') , 
                              'cpc', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_medium'] == 'Inmail') & (df['has_gclid'] == '0') , 
                              'social', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_medium'] == 'Facebook_Marketplace') & (df['has_gclid'] == '0') , 
                              'social', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_source'] == '4geeks') & (df['has_gclid'] == '0') , 
                              'social', df['utm_medium'])

    df['utm_medium'] = np.where((df['utm_medium'] == 'rrss') & (df['has_gclid'] == '0') , 
                              'social', df['utm_medium'])
    
    return df
  
#Visualization features
    
def countplot_features(df, feature):
    fig = plt.figure(figsize=(10,6))
    ax = sns.countplot(x=df[feature], order=df[feature].value_counts(ascending=False).index);

    abs_values = df[feature].value_counts(ascending=False).values
    ax.bar_label(container=ax.containers[0], labels=abs_values)
    plt.xticks(rotation=30, ha='right')
    #plt.show()
    
def countplot_targetvsfeature(df,feature,target):
    fig = plt.figure(figsize=(10,6))
    ax = sns.countplot(x=df[feature], hue=target, order=df[feature].value_counts(ascending=False).index);

    abs_values = df[feature].value_counts(ascending=False).values
    ax.bar_label(container=ax.containers[0], labels=abs_values)
    plt.xticks(rotation=30, ha='right')
    #plt.show()