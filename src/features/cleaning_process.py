import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

import build_features as bf

from constants import TO_DROP

#Loading the data
data = pd.read_csv('../../data/raw/All_Form_Entries.csv', dtype={'utm_content': 'object', 
                                                              'current_download': 'object', 
                                                              'state': 'object', 'lead_type': 'object',
                                                              'lead_generation_app':'object'})

#Changing type of columns 
bf.change_to_datetime(data,'created_at')
bf.change_to_datetime(data,'updated_at')
bf.change_to_datetime(data,'won_at')

#Changing format
bf.change_format(data,'created_at')
bf.change_format(data,'updated_at')
bf.change_format(data,'won_at')

#Format change also changed the column type to object, so we need to convert it to datetime again 
bf.change_to_datetime(data,'created_at')
bf.change_to_datetime(data,'updated_at')
bf.change_to_datetime(data,'won_at')

#creating new columns
data['year-month'] = data['created_at'].dt.strftime('%Y-%m')
data['created_time'] = data['created_at'].dt.strftime('%H:%M:%S')
data['has_gclid'] = np.where(data['gclid'].isnull(), '0', '1')

#Combine first and last name ignoring nulls
bf.combine_columns(data, 'first_name', 'last_name', 'fullname')

# shift column 'Fullname' to third position
fourth_column = data.pop('fullname')
data.insert(3, 'fullname', fourth_column)
data.drop(['first_name', 'last_name'], axis=1, inplace=True)

#drop null columns
bf.drop_null_columns(data)

#drop irrelevant columns
data.drop(TO_DROP, inplace=True, axis=1)

#drop testing rows
bf.drop_test_rows(data)

#dropping two other test rows identified
data.drop(data[data['utm_source'] == 'test_s'].index, inplace = True)
data.drop(data[data['utm_source'] == 'fintech'].index, inplace = True)

#remove duplicated rows by combining them considering the first creation date
bf.remove_duplicates(data)

#Clean course column
bf.clean_course(data,'course')

#Clean location column
bf.clean_location(data,'location')

#clean language column
bf.clean_language(data,'language')

#clean utm_medium
bf.clean_utm_medium(data,'utm_medium')

#clean utm_source
bf.clean_utm_source(data,'utm_source')

# Assign values
bf.assign_lead_type(data, 'tags','lead_type')

bf.assign_with_conditions(data)

print(data.shape)