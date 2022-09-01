import pandas as pd
import numpy as np

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
    print('shape before combining duplicates: ', df.shape)
    df = df.replace("Nan", np.nan).copy()
    df = df.sort_values("created_at").copy()
    df = df.groupby("email").first().reset_index()
    print('shape after combining duplicates: ', df.shape)
    return df
    
def clean_course(df,column):
    df[column] = df[column].replace(['full-stack-ft', 'full_stack', 'full-stack,software-engineering',
                                    'coding-introduction','outcomes'], 'full-stack')
    df[column] = df[column].replace(['machine-learning', 'machine-learning-enginnering'], 
                                    'machine-learning-engineering')
    print(df[column].value_counts())
    return df
 
def clean_location(df,column):
    df[column] = df[column].replace(['maracaibo'], 'maracaibo-venezuela')
    df[column] = df[column].replace(['los-cortijos-caracas'], 'caracas-venezuela') 
    print(df[column].value_counts())
    return df
  
    
def clean_language(df,column):
    df[column] = df[column].replace('us', 'en')
    print(df[column].value_counts())
    return df
    
    
def clean_utm_source(df,column):
    df[column] = df[column].replace('LInkedin', 'linkedin')
    df[column] = df[column].replace('CourseReport', 'coursereport')
    df[column] = df[column].replace(['landingjobs?utm_medium=machine-learning-engineering', 
                                    'landingjobs?utm_medium=full-stack', 'landingjobs?utm_medium=RRSS'],
                                    'landingjobs')
    df[column] = df[column].replace('google_ads', 'google')
    df[column] = df[column].replace(['Instagram_Feed', 'ig', 'Business Manager IG','23848557212380143',
                                    '23849317251630143', 'Instagram_Stories'], 'instagram')
    df[column] = df[column].replace(['23848655532190143','23850705303260143','23850859670310143','23850859616000143','Facebook','Facebook ads','Facebook_Mobile_Feed',
                                    'facebook_instagram','fb','Facebook_Desktop_Feed','facebook_awareness',
                                    'Facebook_Marketplace','Facebook_Stories','cpc','an'],
                                    'facebook')
    df[column] = df[column].replace(['PR?utm_medium=nota-prensa-1','python-es'], '4geeks' )
    print(df[column].value_counts())
    return df


def clean_utm_medium(df,column):
    df[column] = df[column].replace(['schoolpage','coursereportschoolpage', 'schoolpage?utm_source=careerkarma',
                                    'Blog','affiliate_email'], 'referral')
    df[column] = df[column].replace(['23849575173750143','ppc','Instagram_Feed','FB paid','Instagram_Stories',
                                     'ML + AI','ML + AI v2 - 3rd time (Mar, lookalike NYC, NJ)'],
                                    'cpc')
    df[column] = df[column].replace('lead gen','social') 
    df.loc[df['utm_source'] == 'landingjobs', column] = 'referral'
    print(df[column].value_counts())
    return df      
    

def assign_lead_type(df,column1,column2):
    df.loc[df[column1] == 'request_more_info', column2] = 'SOFT'
    df.loc[df[column1] == 'website-lead', column2] = 'STRONG'
    df.loc[df[column1] == 'newsletter', column2] = 'DISCOVERY'
    df.loc[df[column1] == 'contact-us', column2] = 'SOFT'
    df.loc[df[column1] == 'utec-uruguay', column2] = 'STRONG'
    df.loc[df[column1] == 'jobboard-lead', column2] = 'STRONG'
    df.loc[df[column1] == 'hiring-partner', column2] = 'OTHER'
    df.loc[df[column1] == 'download_outcome', column2] = 'DISCOVERY'
    df.loc[df[column1] == 'website-lead,blacks-in-technology', column2] = 'STRONG'
    df.loc[df[column1] == 'request_downloadable', column2] = 'DISCOVERY'
    print(df[column2].value_counts())
    return df

def assign_with_conditions(df):
    df['utm_medium'] = np.where((df['utm_medium'] == 'Facebook_Mobile_Feed') & (df['has_gclid'] == '0'), 
                                'organic', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'Facebook_Mobile_Feed') & (df['has_gclid'] == '1') , 
                                'cpc', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'Facebook_Marketplace') & (df['has_gclid'] == '0'), 
                                'organic', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == '23849757712110143') & (df['has_gclid'] == '0'), 
                                'organic', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == '23849757712110143') & (df['has_gclid'] == '1'), 
                                'cpc', df['utm_medium'])
     
    df['utm_medium'] = np.where((df['utm_medium'] == 'Inmail') & (df['has_gclid'] == '0'), 
                              'organic', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'inscripcion') & (df['has_gclid'] == '0'), 
                              'social', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'event') & (df['has_gclid'] == '0'), 
                              'social', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'lead gen') & (df['has_gclid'] == '0'), 
                              'organic', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'rrss') & (df['has_gclid'] == '0') , 
                              'organic', df['utm_medium'])
    
    df['utm_medium'] = np.where((df['utm_medium'] == 'rrss') & (df['has_gclid'] == '1') , 
                              'cpc', df['utm_medium'])
       
    print('Assignation with conditions ok')
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